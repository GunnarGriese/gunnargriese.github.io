---
layout: post
title: Automating GTM Server-Side Container Updates on Cloud Run
description: A Python Cloud Run Function that automatically checks Google's container registry for new stable sGTM images and updates your Cloud Run services across GCP projects, preserving all existing configuration.
author: gunnar
date: 2026-04-27 00:00:01 +0200
categories: [GTM]
tags: [gtm-server-side, gcp]
image: /assets/images/blog/sgtm-cr-updater.png
comments: true
toc: true
lang: en
---

If you're running server-side Google Tag Manager (sGTM) on Cloud Run, you've probably asked yourself at some point: "Am I even on the latest version?" And if you manage sGTM across multiple GCP projects (say, one per client or one per environment), that question quickly turns into: "How do I keep all of these up to date without manually checking and redeploying each one?"

The honest answer for most of us is: you don't. You deploy sGTM once, it works, and then you forget about it until something breaks or someone asks. Google doesn't auto-update your Cloud Run container images. There's no notification when a new stable version drops. And the official documentation doesn't really cover how to handle ongoing maintenance at scale.

This is the problem I set out to solve with the **sGTM Cloud Run Updater** — a Cloud Run Function that automatically checks Google's container registry for the latest stable sGTM image and updates your Cloud Run services if a newer version is available. It works across GCP projects, preserves your existing service configuration, and can be scheduled to run daily via Cloud Scheduler.

In this post, I'll walk you through the architecture, the implementation, and how to set it up for your own infrastructure. Let's get into it!

{% include newsletter-cta.html %}

## Why keeping sGTM updated matters

Before diving into the solution, let me briefly explain why this matters in the first place. Google's sGTM container image receives updates that include bug fixes, performance improvements, and new features (like support for new APIs or template capabilities). Running an outdated version means you might miss out on these improvements or, worse, run into issues that have already been fixed upstream.

The sGTM UI helps with by providing a clear warning in the container settings section, but you're probably not frequenty checking here:
![Outdated Image Warning in sGTM UI](/assets/images/gtm-ss-updater/gtm-ui-outdated.png)
_Example of an outdated image warning in the sGTM UI_

In a typical GCP setup, you'd need to:

1. Manually check Google's container registry (`gcr.io/cloud-tagging-10302018/gtm-cloud-image`) for new versions
2. Compare the current image SHA against the latest `stable` tag
3. Update your Cloud Run service with the new image
4. Verify that the new revision is serving traffic correctly

Now multiply that by the number of sGTM services you manage. For one of my clients, that's more than a handful across different regions and markets. And this is exactly where the need for an automated solution was born. Because if I were to be doing this manually, it simply wouldn't work for long. The process isn't just tedious — it's the kind of task that simply doesn't get done regularly because there's always something more pressing to deal with.

At the same time, the side effects of not updating can result in breaking issues as I had to learn the hard way a couple of years ago when one of the template APIs wasn't properly supported by one of the older images. But yeah, let's not go there (😉). It's just to say I've learned my lesson and thrive to keep sGTM images up-to-date whereever I can.

## Credit where credit is due

Before doing anything else, I have to point out that the core idea and approach behind this project come from the brilliant [Moritz Bauer](https://github.com/Liscor), who originally built an [sGTM Cloud Run Updater](https://github.com/Liscor/sgtm_cloud_run_updater) in Node.js. The logic is the same: query Google's container registry for the latest stable SHA, compare it against the deployed revision, and update if they differ. His blog is currently undergoing a relaunch. Therefore, the detailed solution is currently unfortunately not available, so I wanted to document the approach here.

The version I present in this blog post is essentially a Python port (since that's my go-to language for Cloud Run Functions) with a few practical additions: health probe validation that checks whether probes actually have an action set before copying them to the new revision, structured logging with per-service context prefixes for easier debugging across multiple targets, and a proper CI setup with unit tests, linting, and type checking.

## Architecture Overview

The architecture is deliberately simple. It's a single Cloud Run Function deployed in a central GCP project that can reach out to Cloud Run services in multiple target projects. Cloud Scheduler triggers the function on a schedule (e.g., daily at 06:00), passing the target service details as a JSON payload.

![sGTM Cloud Run Updater Architecture](/assets/images/gtm-ss-updater/cloud-run-updater-architecture.png)
_sGTM Cloud Run Updater Architecture_

Here's the flow:

1. **Cloud Scheduler** fires a POST request to the Cloud Run Function with the target service's `project_id`, `region`, and `service_name`
2. The **Cloud Function** lists the revisions of the target Cloud Run service and identifies the currently active one
3. It extracts the **image SHA** from the active revision's container configuration
4. It queries **Google's container registry** (`gcr.io`) for the manifest of the `gtm-cloud-image` and finds the SHA tagged as `stable`
5. If the SHAs match, it returns a 200 (= no update needed)
6. If they differ, it **creates a new revision** with the updated image while preserving all existing configuration (environment variables, resource limits, health probes, scaling settings)
7. It then **polls** the service (every 10 seconds, up to 5 minutes) until the new revision becomes active

> If you're managing sGTM across multiple GCP projects (which is common in agency or consultancy setups), this architecture scales well. You deploy the Cloud Run Function once in a central project and create one Scheduler job per target service. The cross-project access is handled via IAM — the Cloud Function's service account just needs `roles/run.admin` in each target project.

## Implementation Deep Dive

Let me walk you through the key parts of the implementation. The full source code is available on [GitHub](https://github.com/daidalytics/sgtm-cr-updater), but I'll highlight the interesting bits here.

### Fetching the Latest Stable Image

The function queries Google's container registry to find the SHA of the image tagged as `stable`:

```python
GCR_TAGS_URL = "https://gcr.io/v2/cloud-tagging-10302018/gtm-cloud-image/tags/list"

def _fetch_stable_image_sha() -> tuple[str | None, list[str] | None]:
    """Fetch the latest stable GTM image SHA and tags from GCR."""
    response = requests.get(GCR_TAGS_URL, timeout=30)
    response.raise_for_status()

    manifest = response.json().get("manifest", {})
    for release_key, release_info in manifest.items():
        tags = release_info.get("tag", [])
        if isinstance(tags, list) and "stable" in tags:
            sha = release_key.split(":")[1] if ":" in release_key else None
            return sha, tags

    return None, None
```

This endpoint is publicly accessible (no authentication required), which makes things straightforward. The function iterates over the manifest entries and looks for the one tagged as `stable`. Google uses this tag to mark the latest validated version of the sGTM container image.

### Comparing Versions

The comparison is done at the SHA level, which is the most reliable way to determine whether two container images are identical:

```python
def _extract_image_sha(image: str) -> str | None:
    """Extract SHA256 hash from a container image string."""
    match = re.search(r"sha256:([a-f0-9]+)", image)
    if match:
        return match.group(1)
    parts = image.split(":")
    return parts[1] if len(parts) > 1 else None
```

Cloud Run stores the full image reference including the SHA (e.g., `gcr.io/cloud-tagging-10302018/gtm-cloud-image@sha256:abc123...`), so we extract that and compare it against the SHA from the registry. Tags can be moved or overwritten — SHAs can't.

### Preserving Service Configuration

This is probably the most important part of the implementation. When you update a Cloud Run service with a new container image, you're essentially creating a new revision. If you're not careful, you might lose configuration that was set on the previous revision. The function explicitly copies over environment variables, resource limits, health probes, and scaling settings from the active revision:

```python
def _build_updated_service(params: dict, active_revision, new_image: str) -> Service:
    """Build an updated service definition preserving config from the active revision."""
    old_container = active_revision.containers[0]

    container_kwargs: dict = {
        "image": new_image,
        "env": old_container.env,
        "resources": old_container.resources,
    }
    if _probe_has_action(old_container.liveness_probe):
        container_kwargs["liveness_probe"] = old_container.liveness_probe
    if _probe_has_action(old_container.startup_probe):
        container_kwargs["startup_probe"] = old_container.startup_probe

    new_container = Container(**container_kwargs)

    return Service(
        name=f"projects/{params['project_id']}/locations/{params['region']}/services/{params['service_name']}",
        template=RevisionTemplate(
            containers=[new_container],
            scaling=RevisionScaling(
                min_instance_count=active_revision.scaling.min_instance_count,
                max_instance_count=active_revision.scaling.max_instance_count,
            ),
        ),
    )
```

The environment variables are particularly critical here since that's where your sGTM container configuration lives — the container config string, preview server URL, and any custom settings you've added. Losing those during an update would effectively break your sGTM deployment.

> Note that service-level settings like `--no-cpu-throttling`, `--allow-unauthenticated`, `--ingress`, and `--timeout` are not affected by revision updates. These persist across revisions automatically, so the function doesn't need to handle them.

### Polling for the New Revision

After triggering the update, the function polls the service to confirm that the new revision has become active:

```python
POLL_INTERVAL_SECONDS = 10
MAX_POLL_ATTEMPTS = 30  # 5 minutes total

def _wait_for_new_active_revision(
    revisions_client, parent, stable_image_key, old_revision_name, svc_logger
) -> bool:
    """Poll until a new revision with the stable image becomes active."""
    for attempt in range(1, MAX_POLL_ATTEMPTS + 1):
        time.sleep(POLL_INTERVAL_SECONDS)

        for revision in revisions_client.list_revisions(parent=parent):
            revision_image = revision.containers[0].image if revision.containers else None
            if not revision_image or stable_image_key not in revision_image:
                continue
            if revision.name == old_revision_name:
                continue

            for condition in revision.conditions:
                if condition.type_ == "Active" and condition.state.name == "CONDITION_SUCCEEDED":
                    svc_logger.info("New revision %s is now active", revision.name)
                    return True

        svc_logger.info("Attempt %d/%d: New revision not yet active...", attempt, MAX_POLL_ATTEMPTS)

    return False
```

This gives the update up to 5 minutes to complete. In practice, Cloud Run revision deployments typically take 30-60 seconds for sGTM containers, so this is plenty of headroom. If the timeout is reached, the function returns a 202 (accepted but not yet confirmed) rather than treating it as an error — because the update was initiated successfully, it just hasn't been confirmed yet.

## Setting It Up

So, now that we've covered how it works, let's look into how to deploy the setup.

### Prerequisites

You'll need:

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager (or `pip`)
- Google Cloud SDK (`gcloud`)
- A GCP project with Cloud Run Functions API, Cloud Run Admin API, and Cloud Build API enabled

### Deployment

Deploy the Cloud Run Function to your central GCP project:

```bash
gcloud functions deploy sgtm-cr-updater \
  --gen2 \
  --runtime=python312 \
  --region=europe-west1 \
  --source=. \
  --entry-point=check_cloud_run \
  --trigger-http
```

### IAM Configuration

The Cloud Run Function's service account needs `roles/run.admin` in each target project:

```bash
gcloud projects add-iam-policy-binding TARGET_PROJECT_ID \
  --member="serviceAccount:CF_SERVICE_ACCOUNT@CENTRAL_PROJECT.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```

And the Cloud Scheduler service account needs permission to invoke the function:

```bash
gcloud functions add-invoker-policy-binding sgtm-cr-updater \
  --region=europe-west1 \
  --member="serviceAccount:SCHEDULER_SA@CENTRAL_PROJECT.iam.gserviceaccount.com"
```

### Scheduling Updates

Create one Cloud Scheduler job per target service:

```bash
gcloud scheduler jobs create http update-sgtm-client-a \
  --location=europe-west1 \
  --schedule="0 6 * * *" \
  --uri="CLOUD_FUNCTION_URL" \
  --http-method=POST \
  --headers="Content-Type=application/json" \
  --message-body='{"project_id":"client-a-project","region":"europe-west3","service_name":"sgtm-service"}' \
  --oidc-service-account-email="SCHEDULER_SA@CENTRAL_PROJECT.iam.gserviceaccount.com"
```

This triggers the update check every day at 06:00. Adjust the schedule and region to your needs. The `--oidc-service-account-email` flag ensures the request is authenticated, which is important since the Cloud Run Function requires authentication by default.

## What's Next

The source code is available on [GitHub](https://github.com/daidalytics/sgtm-cr-updater). The repo includes unit tests, CI via GitHub Actions (lint, format, type checks, and tests), and a Cloud Build config for deployment.

A few things I'm considering for future iterations:

- **Slack / email notifications** when an update is performed (or when one fails)
- **Multi-service batch updates** via a single Cloud Scheduler trigger to reduce the number of scheduled jobs
- **Terraform module** for those who prefer Infrastructure-as-Code for the deployment of the updater itself

If you're managing sGTM on Cloud Run, give this a try and let me know how it works for your setup. And if you spot something that could be improved, feel free to [open an issue](https://github.com/daidalytics/sgtm-cr-updater/issues) or submit a pull request.

Happy deploying!

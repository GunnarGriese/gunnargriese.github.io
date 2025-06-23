---
title: GTM Server-Side Pantheon - Part 4 - Monitoring GTM Server-Side Data Flows
author: gunnar
date: 2025-10-30 00:00:01 +0200
categories: [GTM]
tags: [gtm-server-side]
comments: true
toc: true
lang: en
---

It seems like I prematurely announced the grand finale of my series about the GTM Server-Side (sGTM) Pantheon in my [latest blog post](https://gunnargriese.com/posts/gtm-server-side-vertex-ai/) in that series. 

After all, it turns out that the sGTM Pantheon is a gift that keeps giving. Lately, the (apparently) tireless Google engineers from the gTech Ads team added not one, not two, but three new templates to the gallery and, by doing so, guiiding my pen back to paper.

One good thing came out of these unexpected additions to the Pantheon already: I might have understood why the Google team chose references to Greek mythology! Besides the twelve principal deities, there are literally hundreds of other gods and goddesses, titans, nymphs, and satyrs (you might want to check out [this website](https://www.theoi.com/) to get a complete overview). So, it's definitely enough to have a good number of names to choose from for all the future potential sGTM templates to come.

## What's new in the sGTM Pantheon?
But there's more to it. With the latest additions, the Google team introduced a new category of solutions to the Pantheon.

The Pantheon solutions so far have been focused on either **enriching the data flow in real -time** with data points from [Firestore](https://gunnargriese.com/posts/gtm-server-side-firestore-integrations/), [Google Sheets](https://gunnargriese.com/posts/gtm-server-side-bigquery-google-sheets/), or [Vertex AI](https://gunnargriese.com/posts/gtm-server-side-vertex-ai/) or **sending data points to destinations** like [BigQuery](https://gunnargriese.com/posts/gtm-server-side-bigquery-google-sheets/), [PubSub](https://gunnargriese.com/posts/gtm-server-side-pubsub-integration/), or [Google Sheets](https://gunnargriese.com/posts/gtm-server-side-bigquery-google-sheets/). 

The three new tag templates are targeted at making sure that all the potential data flows and orchestrations running on sGTM are fully functional and can be monitored on an ongoing basis. 

> If you've followed me for some time already, you might have read my [previous blog post](https://gunnargriese.com/posts/ga4-data-quality-at-scale/) on why you should monitor your sGTM data flows. If not, I highly recommend it as an introduction to this post.

But now, without further ado let me briefly introduce the latest tag templates to you:

* **Argos**: Comprehensive monitoring system for gTag configurations with multi-destination error logging (sGTM console, GA4, BigQuery, and Cloud Logging). Convers domain, region, consent, privacy settings, and gTag measurement ID configuration parameters.
* **Theia**: Zero-code logging solution that simplifies data surfacing in preview mode and streamlines record-keeping through Cloud Logging integration.
* **Zeus**: Advanced container tag monitoring tool that tracks event success/failure metrics with flexible logging options across preview mode, Cloud Logging, and BigQuery environments.

Let's take a closer look at these solutions individually to see how they can help us in our day-to-day work.

## Argos - The tireless watchman

In Greek mythology Argos is a many-eyed giant serving as Hera's perpetual watchman. Like its namesake the [tag template](https://github.com/google-marketing-solutions/gps-sgtm-pantheon/blob/main/sgtm/argos/README.md) is designed to constantly overseeing your sGTM setup. In particular, the tag allows you to perform a set of basic checks on top of your GA4 data stream and log any issues that might arise into GA4, BigQuery, and/or Cloud Logging. The tag template allows you to specify a set of expected values for certain data points that are then compared with the actual data that is sent to the sGTM container with a given GA4 event.

![Argos Tag Template](/assets/img/gtm-ss-monitoring/argos-tag-template.png)
_Argos Tag Template_


As you can see from the tag screenshot above, the out-of-the-box checks cover:

* **Expected Domains**: Check the domain derived from the event's `page_location` against a comma-separated list of allowed domains for your GA4 measurement ID.
* **Expected Countries**: Check the event's `event_location.country` value against a comma-separated list of allowed countries for your GA4 measurement ID. (This requires [serving Google scripts from sGTM](https://developers.google.com/tag-platform/tag-manager/server-side/enable-region-specific-settings))
* **Expected GA4 Measurement IDs**: Check the event's `x-ga-measurement_id` value against a comma-separated list of allowed GA4 measurement IDs.
* **Expected DMA parameter value**: Check the event's `x-ga-dma` value against a dropdown (1, 0, or both). `x-ga-dma` = 1 is expected for EEA traffic and 0 for non-EEA traffic. GA4 applies different data controls to EEA traffic.
* **Expected GCS value**: Check the event's `x-ga-gcs` value against a comma-separated list of allowed values (e.g., G101, G111, etc.). (This requires a Consent Mode implementation. See [here](https://gunnargriese.com/posts/consent-mode-v2/#gcs-parameter) for a full list of potential value expressions.)


The reason that these are chosen is that faulty values for these particular gTag settings can cause potentially large discrepancies within your GA4's reporting, bidding, audiences and negatively impact your business' other marketing platforms as well (e.g., Google Ads). The side effects range from faulty attribution, non-functional audiences, or even missing/wrong data in your GA4 property. 

> Should you be interested in the details, I can recommend checking out the [`README.md` file]((https://github.com/google-marketing-solutions/gps-sgtm-pantheon/blob/main/sgtm/argos/README.md#explanation-of-settings-in-detail)) in the Github repository, which provides a more detailed overview of the implications.   

The underlying mechanics of the template are quite straightforward. For the checks itself, the template takes advantage of the [`getEventData` API](https://developers.google.com/tag-platform/tag-manager/server-side/api#geteventdata) to obtain a specific value from the data made available via an incoming event. This value is than evaluated against the template's inputs and either passes the test - meaning we are dealing with an expected value - or it fails, and a respective error message is created.

See the below excerpt from the tag's Sandbox JS code to get an idea of this process:

```js
/* 
EXEMPLARY CHECKS PERFORMED BY THE ARGOS TAG TEMPLATE
*/

//Set up variables to track errors
let errorMessage = "Errors: ";
let shortErrorMessage = "";
let numErrors = 0;

//Check domains
if(data.expectedDomains) {
  const requestDomain = extractDomain(getEventData("page_location"));
  if(!isValueInList(data.expectedDomains, requestDomain)) {
    errorMessage += "Request sent by unlisted domain. Expected: " + data.expectedDomains + " but got " + requestDomain + ". ";
    shortErrorMessage += "domains;";
    numErrors++;
  }
}

//Check expected GA measurement IDs
if(data.expectedGAMeasurmentIds) {
  const requestGaMeasurementId = extractDomain(getEventData("x-ga-measurement_id"));
  if(!isValueInList(data.expectedGAMeasurmentIds, requestGaMeasurementId)) {
    errorMessage += "Request sent by unlisted GA4 Measurement ID. Expected: " + data.expectedGAMeasurmentIds + " but got " + requestGaMeasurementId + ". ";
    shortErrorMessage += "ga4measurmentIds;";
    numErrors++;
  }
}
```
Now, that the tag has evaluated the event data object against the specified set of rules, it needs to make potential error messages available to us for further analysis or alerting. For this purpose, the event gives us three options (s. `Actions` group in the tag's screenshot above):

* **Send error event to GA4**: This allows you to specify an event name and send the event to a GA4 property of your choice (optional: include a custom dimension with the `shortErrorMessage` (s. code snippet above)). 
* **Log incoming request and associated error (message) to BigQuery**: 
* **Log incoming request and associated error (message) to Cloud Logging**: 

![Argos Error Logging in GA4 & BigQuery](/assets/img/gtm-ss-monitoring/ga4-bq-error-logs.png)

The Argos template gives you the same modularity and flexibility I've mentioned in previous sGTM Pantheon templates. In the example below, I've enhanced the standard configuration by adding two custom checks: one that validates incoming event names against my predefined whitelist, and another that ensures the items array maintains proper formatting with at least an `item_id` or `item_name` parameter present.

![Argos Tag Template Modified](/assets/img/gtm-ss-monitoring/argos-tag-template-modified.png)
_Argos Tag Template Modified_

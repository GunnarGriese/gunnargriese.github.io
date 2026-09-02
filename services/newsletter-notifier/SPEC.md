# Spec: Newsletter Notifier

## Objective

Gunnar has been collecting subscriber emails via the blog's newsletter signup form (`_includes/newsletter-signup.html` → `assets/js/newsletter.js` → the existing `website-form-to-bq` Cloud Function → BigQuery). There is currently no way to actually email those subscribers.

This project builds the **sending side**: a manually-run local Python script that takes a hand-written announcement (subject + body, as Markdown, living in this repo), reads the current subscriber list from BigQuery, renders the content into an email, and sends it via a third-party email API — plus one small deployed endpoint so recipients can unsubscribe with one click (this piece can't run locally, since it must be a publicly clickable URL).

**Users:** Gunnar only (operator triggering sends via CLI). Subscribers are the email recipients — a small (< a few hundred) list of blog readers who opted in via the signup form.

**Success looks like:** Gunnar can add a Markdown file to this repo, run one local command with `--dry-run` to preview who would receive what, then run it again for real, and every subscriber who hasn't unsubscribed gets a well-formed email with a working unsubscribe link — without ever touching subscriber data by hand, deploying anything to send, or risking an accidental blast.

**Explicitly out of scope:** the signup form/capture flow (already exists), any change to the BigQuery ingestion function, and automatic triggering on blog-post publish (may be a future enhancement, not this spec).

## Tech Stack

- **Language:** Python 3.11+ (matches the repo's existing `google-cloud-bigquery` / `functions-framework` usage in the root `requirements.txt`)
- **Compute:**
  - **Sender:** local Python script, run manually from your machine — no deployment, no build step. Talks to BigQuery using Application Default Credentials (`gcloud auth application-default login`) and calls the email API directly (SDK or plain HTTPS request).
  - **Unsubscribe handler:** the one piece that must be deployed, since it's a link recipients click from their inbox. A single Cloud Function (`functions-framework`, matching the convention already used by `website-form-to-bq`) exposing `GET /unsubscribe?token=...` — smallest-effort option, no need for a full Cloud Run service.
- **Data source:** BigQuery (existing subscriber table populated by `website-form-to-bq`)
- **Content source:** a Markdown file living in this repo (frontmatter: `subject`, plus a Markdown body) — no GCS needed now that the sender runs locally
- **Email provider:** **Brevo** (recommended — see rationale below)
- **Secrets:**
  - Sender (local): Brevo API key in a local `.env` file, gitignored, loaded via `python-dotenv` — never committed
  - Unsubscribe handler (deployed): unsubscribe signing key in GCP Secret Manager, injected as an env var at runtime
- **Project/region:** same GCP project and region as the existing signup function (`nlp-api-test-260216`, `europe-west1`) unless Gunnar says otherwise — relevant only to the unsubscribe handler deployment and to BQ dataset location

### Email provider rationale

Given: small list (well under any free tier), EU-based sender, content that is a genuine bulk/marketing-style announcement (not transactional), and a requirement to build real unsubscribe handling ourselves:

| Provider | Why / why not |
|---|---|
| **Brevo (chosen)** | EU company (Sendinblue), explicit GDPR posture matches EU-based sending; free tier (300/day ≈ 9,000/mo) is far more than needed; official Python SDK; supports both transactional and marketing sends without ToS friction. |
| Postmark | Explicitly discourages/suspends accounts for bulk marketing-style sends — **not suitable** for this use case despite good deliverability. |
| SendGrid / Mailgun | Both viable fallbacks (solid Python SDKs, adequate free tiers) if Brevo's EU data handling or API doesn't fit once implementation starts. |
| SendPulse | Largest free tier (15,000/mo) — worth a second look only if Brevo's daily cap ever becomes a real constraint (unlikely at this list size). |

This is a recommendation, not a lock-in: the provider client should sit behind a small internal interface (`send_email(to, subject, html, text)`) so swapping providers later doesn't touch the rest of the code.

### Confirmed Brevo API integration (researched against official docs)

- **Sending mechanism:** the **batch transactional send** endpoint (`POST /v3/smtp/email` with `messageVersions`), not the Contacts/Campaigns product. It accepts up to 1,000 personalized message versions per call — one call covers our whole list — each with its own `to` and a `params` object, which is how the per-recipient unsubscribe link gets injected into `htmlContent`.
- **No Contacts sync needed:** the batch endpoint sends directly to whatever addresses are passed in `to` — recipients don't need to exist as Brevo "Contacts" first. This means the Brevo Contacts/Import API is **not used** by this project; BigQuery remains the sole subscriber list, with no second copy living in Brevo. (Simplifies the design vs. the original plan — no contact-sync step.)
- **Content:** `htmlContent` / `textContent` are passed inline in the request body — no template upload step required.
- **Unsubscribe caveat (important):** Brevo adds a `List-Unsubscribe` header to every email automatically, which is a free bonus (some inboxes show a native one-click unsubscribe), but Brevo's own unsubscribe/suppression tracking is internal to Brevo and scoped to its own "transactional" bucket — it has no knowledge of our BigQuery table. If a recipient uses Brevo's native link, Brevo quietly stops delivering to them going forward, but our BQ row would still show them as subscribed. So **our custom flow (per-recipient token → deployed unsubscribe handler → mark the BQ row) remains the primary, authoritative mechanism** — Brevo's header is a redundant safety net, not something the app relies on for correctness.
- Sources: [Send a transactional email](https://developers.brevo.com/docs/send-a-transactional-email), [Batch send transactional emails](https://developers.brevo.com/docs/batch-send-transactional-emails), [How does transactional e-mail unsubscribe work? (Brevo Community)](https://community.brevo.com/t/how-does-transactional-e-mail-unsubscribe-work/2059), [Anti-spam policy](https://www.brevo.com/legal/antispampolicy/).

## Commands

Run from `services/newsletter-notifier/`:

```bash
# One-time local setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
gcloud auth application-default login   # BQ read access
cp .env.example .env                    # then fill in BREVO_API_KEY

# Run tests
pytest

# Lint / format
ruff check .
black --check .

# Preview a send — no emails sent, no BQ writes beyond the read
python -m sender.main --content announcements/2026-09-15-new-post.md --dry-run

# Actually send
python -m sender.main --content announcements/2026-09-15-new-post.md

# Deploy the unsubscribe endpoint (the only thing that needs deploying)
gcloud functions deploy newsletter-unsubscribe \
  --gen2 \
  --runtime python311 \
  --region europe-west1 \
  --source unsubscribe/ \
  --entry-point unsubscribe \
  --trigger-http \
  --allow-unauthenticated \
  --set-secrets UNSUBSCRIBE_SIGNING_KEY=unsub-signing-key:latest
```

## Project Structure

```
services/newsletter-notifier/
  SPEC.md                  → this file
  requirements.txt         → shared deps (google-cloud-bigquery, brevo SDK, python-dotenv, markdown, pytest, ruff, black)
  .env.example             → BREVO_API_KEY=... (committed; real .env is gitignored)
  announcements/           → Markdown files you write per send, e.g. 2026-09-15-new-post.md
  common/
    __init__.py
    subscribers.py         → BQ query: fetch active (non-unsubscribed) subscribers
    content.py             → read + parse an announcement .md (frontmatter + body) from local disk
    render.py              → Markdown → HTML + plaintext email parts, unsubscribe link injection
    email_client.py        → thin wrapper around Brevo's batch transactional-send endpoint (send_email interface; one batch call per send, one messageVersion per subscriber)
    tokens.py              → generate/verify per-subscriber unsubscribe tokens
  sender/
    __init__.py
    main.py                → local CLI entrypoint (argparse): --content, --dry-run
  unsubscribe/
    __init__.py
    main.py                → HTTP entrypoint (functions-framework): verify token, mark subscriber unsubscribed in BQ
  tests/
    test_subscribers.py
    test_content.py
    test_render.py
    test_email_client.py
    test_tokens.py
    test_sender_main.py
    test_unsubscribe_main.py
    fixtures/
      sample_announcement.md
```

## Code Style

- Plain functions over classes — this is a script-shaped batch job and a small HTTP handler, not a framework app. No abstraction layers beyond the `common/` modules above.
- Type hints on all function signatures; `black` formatting; `ruff` for linting.
- Structured logging: log as JSON-serializable dicts to stdout (Cloud Run/Functions ships stdout to Cloud Logging automatically) — e.g. `logging.info(json.dumps({"event": "send_complete", "sent": 42, "failed": 0}))`. Never log full subscriber email addresses in bulk; log counts and, on individual failure, the single failing address.
- Example (subscriber fetch, illustrating the intended shape):

```python
def get_active_subscribers(bq_client: bigquery.Client, contacts_table: str, unsubscribes_table: str) -> list[Subscriber]:
    query = f"""
        SELECT DISTINCT email
        FROM `{contacts_table}`
        WHERE message LIKE 'Newsletter signup from:%'
          AND email IS NOT NULL
          AND email NOT IN (SELECT email FROM `{unsubscribes_table}`)
    """
    rows = bq_client.query(query).result()
    return [Subscriber(email=r.email) for r in rows]
```

## Testing Strategy

- **Framework:** `pytest`, tests live under `tests/`, mirroring `common/`, `sender/`, `unsubscribe/` module names.
- **No real network calls in tests** — BigQuery and the Brevo client are mocked (`unittest.mock` / dependency injection via passed-in clients, not module-level globals). `content.py` reads from a local fixtures folder, so no mocking needed there.
- **No real emails ever sent by the test suite**, including CI.
- Coverage focus:
  - `subscribers.py`: query correctly filters out unsubscribed rows
  - `content.py` / `render.py`: frontmatter parsing, missing-subject error handling, Markdown → HTML/text conversion, unsubscribe link correctly injected per-recipient
  - `email_client.py`: batch request payload shape sent to Brevo (one `messageVersions` entry per subscriber, correct `params`/unsubscribe link per entry, mocked HTTP), error handling on API failure or partial batch failure
  - `tokens.py`: token generation is per-subscriber and stable; verification rejects tampered/invalid tokens
  - `sender/main.py`: `--dry-run` never calls the email client or BQ write path; a real run sends one call per active subscriber and logs a summary
  - `unsubscribe/main.py`: valid token flips the correct BQ row and returns a friendly confirmation page; invalid/expired token returns an error without mutating data
- Manual verification before first production use: run `--dry-run` against a real announcement file and eyeball the rendered preview and recipient count before ever sending for real.

## Boundaries

**Always do:**
- Run `--dry-run` first for any new announcement content and review the recipient count + rendered preview before a real send
- Include a working, per-recipient one-click unsubscribe link (and `List-Unsubscribe` header) in every email
- Load the Brevo API key from the local `.env` (sender) and the unsubscribe signing key from Secret Manager (deployed handler) — never hardcode or commit either
- Use Application Default Credentials (`gcloud auth application-default login`) scoped to BQ read access for local runs, not a downloaded service-account key file
- Exclude any BQ row already flagged unsubscribed from every send, with no override
- Treat BigQuery, not Brevo's own suppression state, as the single source of truth for who is subscribed — Brevo's automatic `List-Unsubscribe` header is a bonus, not something the app relies on
- Validate the announcement `.md` has a `subject` in frontmatter before attempting to send; fail loudly if missing

**Ask first:**
- Before the first real send to the full list
- Before changing the BigQuery subscriber table schema
- Before switching email providers or upgrading to a paid tier
- Before adding automatic/scheduled triggering (this spec is manual local-trigger only)

**Never do:**
- Never send without having run `--dry-run` against that same content at least once
- Never commit `.env`, API keys, signing keys, or subscriber data to the repo (`.env` must be in `.gitignore`)
- Never bypass or remove the unsubscribed-row filter to "just get an email out"
- Never log full subscriber address lists in plaintext in bulk

## Success Criteria

- `python -m sender.main --content announcements/<file>.md --dry-run` prints the recipient count and a rendered email preview, and makes zero calls to the Brevo API
- A real (non-dry-run) local invocation sends the rendered email to every subscriber row where `unsubscribed_at IS NULL`, and logs a final summary of sent/failed counts
- Every sent email renders correctly (subject, HTML body, plaintext fallback) and contains a working unsubscribe link
- Clicking the unsubscribe link hits the deployed Cloud Function, marks that subscriber's BQ row as unsubscribed, and they are excluded from the next send
- No secrets appear anywhere in the repo — `.env` is gitignored and only `.env.example` (with placeholder values) is committed
- `pytest` passes with no real network calls made
- A fresh clone of the repo can go from `pip install -r requirements.txt` to a working `--dry-run` in under a few minutes, with no GCP resource other than BQ read access and (for real sends) the Brevo key

## Open Questions

These need concrete answers before/during implementation — flagging rather than guessing:

1. ~~**BigQuery table**~~ **RESOLVED:** `nlp-api-test-260216.website_requests.contact_form` — `timestamp TIMESTAMP, name STRING, email STRING, message STRING`. This is a **shared log table**, also used by the site's general contact form (same Cloud Function, `website-form-to-bq`), not a dedicated subscriber table — it has no `unsubscribed_at` column, and it contains real contact-form inquiries alongside newsletter signups. Two consequences, both load-bearing:
   - **Subscriber identification:** a row counts as a newsletter subscriber only if `message LIKE 'Newsletter signup from:%'` (the exact prefix `assets/js/newsletter.js` writes) — never treat every row in this table as a subscriber, or real contact-form inquiries get emailed without consent. Query `DISTINCT email` to collapse repeat signups.
   - **Unsubscribe storage:** rather than altering this shared table's schema (which the Boundaries section already gates behind "ask first"), unsubscribes are tracked in a **new, separate table this project owns**: `nlp-api-test-260216.website_requests.newsletter_unsubscribes (email STRING, unsubscribed_at TIMESTAMP)`. `subscribers.py`'s query excludes any email present there (`NOT IN` / anti-join); `unsubscribe/main.py` inserts into it. `contact_form` itself is never written to by this project.
2. **Sending domain**: which domain to send from (e.g. a subdomain of gunnargriese.com) and whether SPF/DKIM/DMARC records are already set up or need to be added for Brevo.
3. ~~**Unsubscribe token scheme**~~ **RESOLVED:** stateless HMAC-SHA256 of the email address (`tokens.py`), computed on demand — no token column needed anywhere, including in the new `newsletter_unsubscribes` table.
4. **Sample announcement content**: whether the email should always include a snippet/link back to the full post, or can be freestanding "news" with no post link at all (affects the `render.py` template) — implemented as optional (`post_url` frontmatter field), so this is really just a content-writing choice per send, not a blocking implementation question.

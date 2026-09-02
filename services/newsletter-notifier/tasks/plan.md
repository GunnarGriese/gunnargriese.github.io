# Implementation Plan: Newsletter Notifier

## Context

`SPEC.md` (in this folder) is the approved spec for a local Python CLI that renders a hand-written Markdown announcement, pulls the active subscriber list from BigQuery, and sends it via Brevo's batch transactional-send API — plus a separately-deployed Cloud Function so subscribers can unsubscribe with one click. Nothing was built before this plan; only `SPEC.md` and a gitignored `.env` (Brevo API key) existed.

**Resolved during planning:** the subscriber source is `nlp-api-test-260216.website_requests.contact_form` (`timestamp`, `name`, `email`, `message`) — a table *shared* with the site's general contact form, not a dedicated subscriber table. This has two consequences baked into the design below:
- A row only counts as a subscriber if `message LIKE 'Newsletter signup from:%'` (the exact prefix `assets/js/newsletter.js` writes) — otherwise real contact-form inquiries would get emailed without consent.
- Unsubscribes are tracked in a **new** table this project owns, `website_requests.newsletter_unsubscribes (email, unsubscribed_at)`, rather than altering the shared `contact_form` table (altering it would need explicit sign-off per the spec's own boundaries, and isn't necessary).

**Environment note:** this machine's active `gcloud` project is `daida-guard`, not `nlp-api-test-260216`, and Application Default Credentials aren't configured. Live BQ access and the Cloud Function deploy require the human's own `gcloud auth application-default login` — those steps are documented but not run by the agent.

## Recommended Approach

Build bottom-up along the real dependency graph, each task shipping its own tests (vertical slices):

```
Task 1: scaffolding/config
   │
   ├─▶ Task 2: tokens.py (HMAC unsubscribe tokens)          ─┐  Phase 1
   └─▶ Task 3: content.py (parse announcement .md)          ─┘  (pure logic)
           │
   ┌───────┼───────────────┐
   ▼                       ▼
Task 4: subscribers.py   Task 5: render.py                      Phase 2
           │                       │
           └───────────┬───────────┘
                        ▼
              Task 6: email_client.py (Brevo batch send)          Phase 3
                        ▼
              Task 7: sender/main.py (CLI: --content, --dry-run)   Phase 4

Task 8: unsubscribe/main.py (needs Task 2 only)                    Phase 5
   ▼
Task 9: deploy Cloud Function + live smoke test (needs human gcloud auth)

Task 10: whole-suite QA + human sign-off gate before first real send   Phase 6
```

### Key design decisions

- **`render.py` renders Markdown → HTML/text once per send**, with a literal `{{ params.unsubscribe_url }}` placeholder; `build_unsubscribe_params(subscriber, ...)` supplies the per-subscriber `params` dict. Matches how Brevo's batch endpoint actually substitutes — confirmed against Brevo's docs.
- **Unsubscribe tokens are stateless HMAC-SHA256** of the email (Task 2) — no stored token column anywhere.
- **Local `.env` and the deployed Cloud Function must share the same `UNSUBSCRIBE_SIGNING_KEY`** — Task 9 verifies this via a live round-trip.
- **`unsubscribe/` gets its own trimmed `requirements.txt`** — `gcloud functions deploy --source unsubscribe/` only reads the one inside that directory.
- **Unsubscribe endpoint is public/unauthenticated** — its BQ write must use `bigquery.ScalarQueryParameter`, never string interpolation.
- **Subscriber query filters by `message LIKE 'Newsletter signup from:%'`, excludes emails in `newsletter_unsubscribes`, and never writes to `contact_form`.**

## Task List

### Phase 0: Foundations
- [x] **Task 1 — Project scaffolding & config** (S). Directory tree; `pyproject.toml` (ruff/black/pytest); `requirements.txt` + `unsubscribe/requirements.txt`; `.env.example` documenting the resolved table names, the still-open sending-domain question, and the signing-key sync requirement.
  - Verify: `pip install -r requirements.txt`; `pytest` (0 tests, exit 0); `ruff check .`; `black --check .`; `git check-ignore -v services/newsletter-notifier/.env`

### Checkpoint 0
- [x] Skeleton installs cleanly; `pytest`/`ruff`/`black` pass on the empty tree.

### Phase 1: Pure logic (no BQ/network)
- [x] **Task 2 — `common/tokens.py`** (S). `generate_token(email, secret)` / `verify_token(email, token, secret)`, HMAC-SHA256, timing-safe compare. Deps: Task 1.
- [x] **Task 3 — `common/content.py`** (S). `parse_announcement(path) -> Announcement(subject, body_md, post_url)` via `python-frontmatter`; typed error if `subject` missing; real test fixtures. Deps: Task 1.

### Checkpoint 1
- [x] `pytest tests/test_tokens.py tests/test_content.py` green; neither module imports BQ/Brevo/network libraries.

### Phase 2: Data + rendering
- [x] **Task 4 — `common/subscribers.py`** (S). `Subscriber(email)` + `get_active_subscribers(bq_client, contacts_table, unsubscribes_table)` — filters by the `message LIKE` pattern, `DISTINCT`, excludes `newsletter_unsubscribes`. `bq_client` injected. Deps: Task 1.
- [x] **Task 5 — `common/render.py`** (M). `render_content(announcement)` + `build_unsubscribe_params(subscriber, base_url, secret)`. Deps: Task 2, Task 3.

### Checkpoint 2
- [x] `pytest tests/test_subscribers.py tests/test_render.py -v` green.

### Phase 3: Delivery
- [x] **Task 6 — `common/email_client.py`** (M). `send_batch(brevo_client, ...) -> BatchSendResult`; injected client; chunks ≤1000; no bulk address logging. Deps: Task 5.
  - Note: the installed `brevo-python==5.0.2` is the newer Fern-generated `brevo` SDK (`Brevo(api_key=...).transactional_emails`, method `send_transac_email`), not the legacy `sib_api_v3_sdk` client the original SPEC research assumed. Its own docstring now caps a single call at 2000 total recipients (99 per message version), looser than the 1000 this task already chunks at, so the ≤1000 chunking here stays valid and conservative — just noting the mismatch for Task 7/9 wiring. Errors surface as `brevo.core.api_error.ApiError` with a `status_code`.

### Checkpoint 3
- [x] `pytest tests/test_email_client.py -v` green; batch payload shape verified against mocks.

### Phase 4: Sender CLI
- [x] **Task 7 — `sender/main.py`** (M). `argparse` (`--content`, `--dry-run`); composition root for real BQ/Brevo clients. Deps: Task 4, 5, 6.
  - Manual (needs human `gcloud` auth): `python -m sender.main --content tests/fixtures/sample_announcement.md --dry-run`
  - Note: `main()` only constructs the Brevo client and reads `BREVO_API_KEY`/`SENDER_EMAIL`/`SENDER_NAME` when `--dry-run` is absent, matching SPEC.md's success criterion that a fresh clone can `--dry-run` with only BQ read access. `SENDER_EMAIL`/`SENDER_NAME` still need adding to `.env.example` (blocked for the agent by the local `guard-sensitive-files.sh` hook — human to add).

### Checkpoint 4
- [x] `pytest tests/test_sender_main.py -v` green.

### Phase 5: Unsubscribe handler + deploy
- [ ] **Task 8 — `unsubscribe/main.py`** (M). `mark_unsubscribed` (parameterized INSERT into `newsletter_unsubscribes`) + `unsubscribe(request)` functions-framework entrypoint. Deps: Task 2.
- [ ] **Task 9 — Deploy + live smoke test** (S, needs human `gcloud` auth). Create `newsletter_unsubscribes` table if absent; provision `UNSUBSCRIBE_SIGNING_KEY` in Secret Manager matching `.env`; `gcloud functions deploy` per SPEC.md; curl smoke test.

### Checkpoint 5
- [ ] `pytest tests/test_unsubscribe_main.py -v` green; live deploy verified (human-run).

### Phase 6: Final QA
- [ ] **Task 10 — Whole-suite QA + sign-off gate** (S). Full `pytest`/`ruff`/`black`; one real `--dry-run`, human-eyeballed, before any real send.

### Checkpoint 6 (Done)
- [ ] Every SPEC.md Success Criteria bullet automatically verified or has a recorded manual step.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| `contact_form` mixes contact-form + newsletter rows | High (spam/privacy if mishandled) | Strict `message LIKE 'Newsletter signup from:%'` filter, tested explicitly |
| Local/deployed signing-key drift | High (breaks all sent links silently) | Task 9 verifies via live curl round-trip |
| Sending domain/DNS not yet set up | Deliverability risk on first real send | "Ask first" gate in Task 10 |
| No live GCP access in this environment | Blocks Tasks 7/9/10's manual/live steps | Documented as human-run steps, not agent-run |
| Brevo API key read into a planning tool transcript | Med | Rotate the key in Brevo's dashboard (independent of this plan) |

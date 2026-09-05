---
layout: post
title: The GA4 Data API Quietly Grew a Chat Endpoint - Here's What the API Watch Caught
description: Google's GA4 Data API v1alpha discovery doc just added an undocumented chat method and a chatbot-only OAuth scope. Here's what it looks like, what's conspicuously missing from its description, and where a conversational GA4 endpoint actually fits.
author: gunnar
date: 2026-09-05 00:00:01 +0200
categories: [GA4, GA]
tags: [ga4, ga-cli]
image: /assets/images/blog/ga-cli-chat-endpoint.png
comments: true
toc: true
lang: en
permalink: /posts/ga4-chat-endpoint/
---

Google just added a `chat` method to the GA4 Data API's alpha discovery document, no announcement, no changelog entry, nothing on the release notes page. I only know because GA CLI's weekly discovery-doc watch flagged the diff. It's a conversational interface bolted directly onto GA4's reporting API, and the way Google described (and didn't describe) it tells you almost as much as the endpoint itself.

{% include newsletter-cta.html %}

## How Does GA CLI's API Watch Actually Work?

In the [GA CLI launch post](https://gunnargriese.com/posts/google-analytics-cli/), I mentioned that the project "includes an automated API watch workflow that monitors Google's Discovery documents for changes on a weekly basis." This post is that workflow actually paying off, so let's briefly recap what it does.

Google publishes machine-readable Discovery documents for both the Admin API and the Data API, across their stable and alpha/beta channels. A scheduled job pulls all four every week and diffs the result against last week's snapshot:

```python
DISCOVERY_URLS = {
    "analyticsadmin_v1beta": "https://analyticsadmin.googleapis.com/$discovery/rest?version=v1beta",
    "analyticsadmin_v1alpha": "https://analyticsadmin.googleapis.com/$discovery/rest?version=v1alpha",
    "analyticsdata_v1beta": "https://analyticsdata.googleapis.com/$discovery/rest?version=v1beta",
    "analyticsdata_v1alpha": "https://analyticsdata.googleapis.com/$discovery/rest?version=v1alpha",
}
```

No polling Google's blog, no waiting for a tweet to surface in my feed. If a method, a scope, or a schema changes anywhere in these four documents, I know about it within a week. This time, the diff on `analyticsdata_v1alpha` was not a small one.

## What's New: A Conversational Endpoint for GA4 Data

The new method is `analyticsdata.properties.chat`, reachable at `POST v1alpha/{+property}:chat`. It takes a single required path parameter (`property`, in the familiar `properties/{property}` format) and comes gated behind a brand-new OAuth scope:

```
"https://www.googleapis.com/auth/analytics.chatbot.read": {
  "description": "Query Google Analytics data and insights conversationally"
}
```

Here is Google's method description, in full, because the entire prose Google ships for this endpoint is worth reading exactly once:

> "Provides a chat interface for interacting with Google Analytics data through the API. This product uses AI and may display inaccurate info. Your chat activity may be used to improve the product and your use is subject to Google's Terms, AI Use Policy, and Privacy Policy. Learn more about Chat AI Privacy"

## What's Missing Is as Telling as What's There

Here's where it gets interesting. Every other alpha-stage method in this discovery document, `runFunnelReport`, the audience-list methods, all of them, carries a variation of the same boilerplate: **"introduced at alpha stability with the intention of gathering feedback."** It's Google's standard alpha disclaimer, and it usually comes with a feedback-form link.

`:chat` has neither. No stability disclaimer, no feedback link, nothing pointing you toward a form to report bugs against. I can't tell you definitively what that means (Google doesn't explain its own documentation gaps), but it's a deviation from an otherwise consistent pattern.

The scope story is just as telling. Every read-oriented method elsewhere in this API accepts `analytics` or `analytics.readonly` as valid credentials, exactly what you'd expect for a reporting endpoint. `:chat` accepts neither. The chatbot scope, `analytics.chatbot.read`, is the *sole* accepted credential. Whatever GA's chat feature is doing under the hood, Google apparently doesn't want it authorized under the same trust boundary as `runReport`.

## Request and Response Shapes

Structurally, the endpoint is straightforward. `ChatRequest` looks like this:

| Field | Type | Notes |
|-------|------|-------|
| `userQuery` | string | Required. The user's natural-language question. |
| `sessionId` | string | Optional. Reuse to continue a conversation; invalid IDs error out. |
| `returnPropertyQuota` | boolean | Optional. Include current quota state in the response. |

`ChatResponse` mirrors it:

| Field | Type | Notes |
|-------|------|-------|
| `sessionId` | string | Carry this forward to maintain context. |
| `blocks` | `[ResponseBlock]` | The actual answer, as structured blocks. |
| `propertyQuota` | `PropertyChatQuota` | Only present if requested. |

And the supporting schemas that make up a `ResponseBlock`:

| Schema | Shape | Note |
|--------|-------|------|
| `ResponseBlock` | `text: string`, `table: DataTable` | One block of structured data in the chat response |
| `DataTable` | `headers: [DataTableHeader]`, `rows: [DataTableRow]` | Dimension/metric value combinations, table-style |
| `DataTableHeader` | `header: string`, `dataType: string` | Describes dimension columns; count/order matches the rows |
| `DataTableRow` | `columns: [DataTableCell]` | — |
| `DataTableCell` | `value: string` | Everything arrives stringly-typed |
| `PropertyChatQuota` | `tokensPerHour: QuotaStatus`, `tokensPerDay: QuotaStatus` | Property-level quota, chatbot-specific |

Worth calling out: every value in a `DataTableCell` is a plain `string`, no matter whether the underlying metric is a session count or a currency amount. If you've ever parsed the Data API's regular `runReport` response, this will feel familiar, and it means you're back to casting types yourself before doing anything numeric with the output.

## Where Does `:chat` Actually Fit? Four Use Cases That Hold Up

A conversational reporting endpoint is easy to dismiss as a gimmick, so let's be concrete about where it's genuinely useful instead.

- **Embedded "ask your analytics."** Drop a chat box into a client portal or SaaS dashboard. Zero LLM stack to maintain, zero inference bill, zero schema-grounding work on your end. This is probably the highest value per unit of effort of the four.
- **A tool inside a larger agent.** Expose `:chat` alongside your Stripe, CRM, and ads tools in an agent's toolset. The win here isn't the conversation itself, it's that your supervisor agent never has to hold GA4's schema in context or burn turns recovering from metric/dimension compatibility errors.
- **Hybrid alerting.** This is the pattern I'd actually build: `runReport` on a cron for the deterministic number and the threshold check, and `:chat` for the "why" narrative once that threshold trips. You get auditability where it matters and explanation where it doesn't need to be exact.
- **Chat surfaces and onboarding.** Slack/Teams standup queries, where a few seconds of latency is fine and nobody's reconciling to the cent. Also solid for onboarding people who don't yet know what GA4 even collects.

Notice what's absent from that list: nobody should be routing compliance reporting, billing reconciliation, or anything where you need to defend a number to a client through a "may display inaccurate info" endpoint. Match the use case to the disclaimer Google actually put in writing.

## Can You Actually Call `:chat` Right Now?

Curiosity got the better of me, so I pointed a request at the endpoint directly instead of just reading about it in the discovery doc. The response was a 403:

> "The GA4 chat API refused this request. This means either your account lacks access to this property, or the chat feature is not enabled for your account. Chat is an alpha feature with limited availability."

So there are two alpha gates here, not one. The method showing up in the discovery doc tells you the API *surface* is alpha. It says nothing about whether the *feature* is available on your property, and by default it isn't. Chat looks to be requiring an alpha-enabled property on top of an alpha-capable client. Seeing `:chat` in the schema and being able to call it are two separate milestones, and only one of them has happened for me so far.

## What This Means for GA CLI

Here's my honest read: I'm not wiring this into GA CLI yet as it's alpha for now, and the 403 makes that an easy call rather than a hard one.

But I'm watching it, and `ga chat` just moved onto the GA CLI backlog for the day access actually opens up. The API watch job will tell me the moment the stability disclaimer shows up, the scope requirements change, or that 403 stops firing, and I can add it safely for your use too. That's exactly the point of building the discovery-doc diffing in the first place: I don't need to guess when GA4's API surface shifts, I get told.

## What's Next

If you've somehow gotten past that 403 and are already building against `:chat`, I'd genuinely like to hear about it, latency, hallucination rate on the numbers, whatever you've run into. And if you haven't read the original [GA CLI post](https://gunnargriese.com/posts/google-analytics-cli/) yet, that's the place to start for the bigger picture on why I'm watching these discovery docs so closely in the first place.

Happy analyzing!

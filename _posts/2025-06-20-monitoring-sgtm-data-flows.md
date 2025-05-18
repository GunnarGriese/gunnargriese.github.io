---
title: GTM Server-Side Pantheon - Part 4 - Monitoring GTM Server-Side Data Flows
author: gunnar
date: 2025-06-30 00:00:01 +0200
categories: [GTM]
tags: [gtm-server-side]
comments: true
toc: true
lang: en
---

Well, it seems like I prematurely announced the grand finale of my series about the GTM Server-Side (sGTM) Pantheon in my [latest blog post](https://gunnargriese.com/posts/gtm-server-side-vertex-ai/) in that series. 

After all, it turns out that the sGTM Pantheon is a gift that keeps giving. Lately, the (apparently) tireless Google engineers from the gTech Ads team added not one, not two, but three new templates to the gallery and, by doing so, practically "forced" me (just kidding) to continue this series.

One good thing came out of these unexpected additions to the Pantheon already: I might have understood why the Google team chose references to Greek mythology! Besides the twelve principal deities, there are literally hundreds of other gods and goddesses, titans, nymphs, and satyrs (you might want to check out [this website](https://www.theoi.com/) to get a complete overview). So, it's definitely enough to have a good number of names to choose from for all the future potential sGTM templates to come.

## What’s new in the sGTM Pantheon?
But there's more to it. With the latest additions the Google team introduced a new category of solutions to the Pantheon.

The Pantheon solutions so far have been focused on either **enriching the  data flow in realtime** with data points from [Firestore](https://gunnargriese.com/posts/gtm-server-side-firestore-integrations/), [Google Sheets](https://gunnargriese.com/posts/gtm-server-side-bigquery-google-sheets/), or [Vertex AI](https://gunnargriese.com/posts/gtm-server-side-vertex-ai/) or **sending data points to destinations** like [BigQuery](https://gunnargriese.com/posts/gtm-server-side-bigquery-google-sheets/), [PubSub](https://gunnargriese.com/posts/gtm-server-side-pubsub-integration/), or [Google Sheets](https://gunnargriese.com/posts/gtm-server-side-bigquery-google-sheets/). 

The three new tag templates are targeted at making sure that all the potential data flows and orchestrations running on sGTM are fully functional and can be monitored on an ongoing basis:

* **Argos**: Comprehensive monitoring system for gTag configurations with multi-destination error logging (sGTM console, GA4, BigQuery, and Cloud Logging). Convers domain, region, consent, privacy settings, and gTag measurement ID configuration parameters.
* **Theia**: Zero-code logging solution that simplifies data surfacing in preview mode and streamlines record-keeping through Cloud Logging integration.
* **Zeus**: Advanced container tag monitoring tool that tracks event success/failure metrics with flexible logging options across preview mode, Cloud Logging, and BigQuery environments.

Let's give these a solutions one-by-one to see how they can help is in our day-to-day work.

## Argos - The perpetual watchman

In Greek mythology Argos is a many-eyed giant serving as Hera's tireless watchman. 

---
title: Mapping GA4 Conversions in BigQuery for Comprehensive Dashboarding
author: gunnar
date: 2024-02-08 00:00:01 +0200
categories: [GA4, BigQuery]
tags: [ga4, bigquery, sql]
comments: true
---

Recently, I found myself in a situation where I needed to use Google Analytics (GA4) conversions in BigQuery (BQ) for a dashboarding project. The dashboard was built on raw GA4 event data extracted from BQ, including data from multiple GA4 properties, each with its own set of conversion events managed by different teams and edited frequently.

The challenge was that the GA4 raw data in BQ does not contain this information, and I had to find a way to get it there. In this post, I will show you different ways to achieve this - including my favorite one.

Read the full article on [IIH Nordic's website](https://iihnordic.com/).

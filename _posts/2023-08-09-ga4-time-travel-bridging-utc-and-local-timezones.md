---
title: GA4 Time Travel - Bridging UTC and Local Timezones
author: gunnar
date: 2023-08-09 09:14:15 +0200
categories: [GA4]
tags: [ga4, bigquery]
comments: true
---

Navigating the intricacies of data in GA4’s raw-data has its own hurdles. A good example is the `event_timestamp` which is logged in microseconds and set in Coordinated Universal Time (UTC). While this standardized approach ensures consistency, it does not always align with the real-world context of events, especially when trying to make the BQ data match the data obtained from the GA4 UI. Hence, converting this timestamp to a property's respective timezone becomes an important step for analysts. Without this conversion, analysts might misinterpret the timing of user interactions, leading to potential inaccuracies in data-driven decision-making.

Take for example below graph, where we compare the number of pageviews per hour between the GA4 UI and BQ. The data from the GA4 UI is based on the property's timezone, while the data from BQ is based on UTC. As a result, the data from BQ is shifted by 2 hours, leading to a discrepancy between the two datasets. This is because the property's timezone is set to UTC+2 (Denmark/Copenhagen), while the data from BQ per default is set to UTC.

![ga4-bq-views](/assets/img/timestamp-conversions/ga4-vs-bq-views.png)
_Source: Own dataset_

Read the full article on [IIH Nordic's website](https://www.iihnordic.com).

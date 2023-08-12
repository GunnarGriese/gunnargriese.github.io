---
title: GA4 Time Travel - Bridging UTC and Local Timezones
author: gunnar
date: 2023-08-09 09:14:15 +0200
categories: [GA4]
tags: [ga4, bigquery]
comments: true
---

Navigating the intricacies of data in GA4’s raw-data has its own hurdles. A good example is the `event_timestamp`, which is logged in microseconds and set in Coordinated Universal Time (UTC). While this standardized approach ensures consistency, it doesn't always align with the real-world context of events, especially when trying to make the BQ data match the data obtained from the GA4 UI. Hence, converting this timestamp to a property's respective timezone becomes an important step for analysts. Without this conversion, analysts might misinterpret the timing of user interactions, leading to potential inaccuracies in data-driven decision-making.

Take for example below graph, where we compare the number of pageviews per hour between the GA4 UI and BQ. The data from the GA4 UI is based on the property's timezone, while the data from BQ is based on UTC. As a result, the data from BQ is shifted by 2 hours, leading to a discrepancy between the two datasets. This is because the property's timezone is set to UTC+2 (Denmark/Copenhagen), while the data from BQ per default is set to UTC.

![ga4-bq-views](/assets/img/timestamp-conversions/ga4-vs-bq-views.png)
_Source: Own dataset_

## Understanding the Microsecond Timestamp in GA4

Within the architecture of GA4, the `event_timestamp` is expressed in microseconds, diving even deeper into time granularity than seconds can. Originating from the Unix epoch — a fixed point in time starting from January 1, 1970 — this timestamp captures the moment an event is logged on GA4's servers. In essence, every event is timestamped with microscopic precision (with a slight delay given the amount of time it takes the event to reach the GA4 server), offering analysts a detailed temporal footprint of all user activities.

To put it into context, 1 second is divided into 1,000,000 microseconds. Having this level of precision makes sense in the context of digital analytics, where events often occur in rapid succession. Additionally, UTC serves as the world's time standard, ensuring a consistent reference point across global systems. By combining the precision of microseconds with the universality of UTC, GA4 can capture and standardize events with great accuracy.

GA4's BigQuery export schema provides the following time-related fields:

| Field name      | Data type | Description                                                                                  |
| --------------- | --------- | -------------------------------------------------------------------------------------------- |
| event_date      | STRING    | The date when the event was logged (YYYYMMDD format in the registered timezone of your app). |
| event_timestamp | INTEGER   | The time (in microseconds, UTC) when the event was logged on the client.                     |

_Source: https://support.google.com/analytics/answer/7029846?hl=en_

While the `event_date` is expressed in the property's timezone, the `event_timestamp` is expressed in UTC. This is important to keep in mind when working with the data and can result in weird discrepancies when comparing them using them in their raw form:

```sql
SELECT
  PARSE_DATE('%Y%m%d',event_date) AS table_date,
  EXTRACT( date
  FROM
    TIMESTAMP_MICROS(event_timestamp) ) AS timestamp_date,
  COUNT(*) AS pageviews
FROM
  `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20230701'
  AND '20230703'
  AND event_name = 'page_view'
GROUP BY
  1,
  2
ORDER BY
  1,
  2 ASC
```

The query above obtains the `event_date` and `event_timestamp` from the GA4 BQ export schema, converting the `event_timestamp` to a date format. We achieve this by first applying BQ's [`TIMESTAMP_MICROS` function](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_micros) to the `event_timestamp` column. The resulting TIMESTAMP value is then passed into BQ Standard SQL's powerful [`EXTRACT` function](https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions#extract), which allows us to extract a various parts of the input timestamp (e.g., DAY, MONTH, YEAR, etc.). In this case, we extract the date from the timestamp using `EXTRACT(date FROM TIMESTAMP_MICROS(event_timestamp))`. This results in a date format that matches the `event_date` format (YYYYMMDD), allowing us to compare the two fields.

The conversion process applied to GA4 data can lead to confusing results though:

| table_date | timestamp_date | pageviews |
| ---------- | -------------- | --------- |
| 2023-07-01 | 2023-07-01     | 43        |
| 2023-07-02 | **2023-07-01** | 1         |
| 2023-07-02 | **2023-07-02** | 24        |
| 2023-07-03 | 2023-07-03     | 186       |

As you can see, it appears that the `event_timestamp` of certain events is one day behind the `event_date` for July 2nd. This is because the `event_timestamp` is expressed in UTC, while the `event_date` is expressed in the property's timezone. As a result, the `event_timestamp` for July 2nd is actually July 1st at 22:00:00 UTC. This is because the property's timezone is set to UTC+2 (Denmark/Copenhagen), meaning that the `event_timestamp` is 2 hours behind the `event_date`. So, our GA4 events seem to be time travelling, but in reality, it's just a matter of timezone conversion.

### The GA4 Timestamp Conversion Process in BigQuery

Luckily for us, the `EXTRACT` function allows us to adjust the `event_timestamp` to the property's timezone by adding the `AT TIME ZONE` clause. This clause allows us to convert the `event_timestamp` to any timezone (see a list of all available time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)), which in this case is UTC+2 (Denmark/Copenhagen). The resulting query looks like this:

```sql
SELECT
  EXTRACT(HOUR
  FROM
    TIMESTAMP_MICROS(event_timestamp) AT TIME ZONE "Europe/Copenhagen") hour_adjusted,
  COUNT(*) AS pageviews
FROM
  `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20210131`
WHERE
  event_name = 'page_view'
GROUP BY
  1
ORDER BY
  1 asc
```

To obtain the right property timezone for our query, we can look at the GA4 property settings in the GA4 interface:

![ga4-timezone-settings](/assets/img/timestamp-conversions/ga4-timezone-settings.png)
_Admin > Property Settings > Reporting time zone_

## Practical Implementation

![heatmap-views](/assets/img/timestamp-conversions/heatmap-views.png)
_Source: Public GA4 BQ dataset_

## Conclusion

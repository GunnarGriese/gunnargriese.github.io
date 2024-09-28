---
title: Mapping GA4 Conversions in BigQuery for Comprehensive Dashboarding
author: gunnar
date: 2024-02-08 00:00:01 +0200
categories: [GA4, BigQuery]
tags: [ga4, bigquery, sql]
comments: true
lang: en
---

Recently, I found myself in a situation where I needed to use Google Analytics (GA4) conversions in BigQuery (BQ) for a dashboarding project. The dashboard was built on raw GA4 event data extracted from BQ, including data from multiple GA4 properties, each with its own set of conversion events managed by different teams and edited frequently.

The challenge was that the GA4 raw data in BQ does not contain this information, and I had to find a way to get it there. In this post, I will show you different ways to achieve this - including my favorite one.

## The Problem

As stated above, the events in the GA4 raw data in BQ do not have an event parameter indicating whether or not they are conversion events. You don't believe me? Go ahead, feel free to pull your GA4 data from BQ and check for yourself...

Now that you're back, you can see that this means the daily raw data exports on its own are insufficient to calculate the number of conversions or a conversion rate for a given property, which is an everyday use case for many analysts and marketers (especially for reporting).

![ga4-ui-conv](/assets/img/ga4-conversions-to-bq/ga4-ui-conv.png)
_Conversion Settings - Own GA4 Property_

The conversion events are defined in the GA4 property settings in the UI and can be adjusted by any team member with `Edit` access to the property at any time. Here is the only place where the information of which event is a conversion is maintained. While this isn't a big deal when you're only dealing with a single GA4 property, keeping your SQL queries and the GA4 settings in sync becomes a real challenge when handling multiple GA4 properties that are managed independently but require some unified reporting.

## The Solution Space

After some research, I came up with three different ways to get the information about conversion events into BQ:

![ga4-conv-to-bq](/assets/img/ga4-conversions-to-bq/ga4-conv-to-bq.png)
_Solution Space Own Visualization_

1. **Manual Approach in SQL**: Manually updating a table or the SQL query in BQ with the conversion events and their properties
2. **Dynamic Approach Using GTM SS**: Using Transformations in Google Tag Manager Server-Side (GTMSS) to add a custom event parameter to the GA4 events indicating whether or not they are conversion events
3. **Dynamic Approach Using GA4 Admin API and GCP**: Using the GA4 Admin API to get the conversion events and then uploading them to BQ

Let's look at these approaches in detail to see how they would work.

## Manual Approach in SQL

Embedding the conversion events in the SQL query is the most straightforward way to get the conversion events into BQ. This approach could be used for properties with infrequently changing conversion events. The actual embedding can be done in many different ways - for example, by using a `WITH` clause, `CASE ... WHEN...` statements or by creating a separate table in BQ.

In the example below I'm using a list of conversions events and evaluate the actual events against the list. If the event is in the list, it's a conversion event and increases the `total_conversions` count by 1.

```sql
SELECT
  COUNT(DISTINCT user_pseudo_id) AS total_users,
  COUNTIF(event_name IN ('click',
      'new_desktop_user',
      'purchase')) AS total_conversions, -- list of conversion events
  COUNT(*) AS total_events
FROM
  `<your-project-id>.analytics_<your-property-id>.events_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20240203'
  AND '20240203';
```

Although this approach appears to be simple to execute at first glance, the obvious downside of it is that you have to update the SQL query every time a conversion event is added, removed or changed. In practice this means that before you can run your SQL query, you have to check if the conversion events have changed and update the SQL query accordingly. This is not only time-consuming but also error-prone. Hence, I cannot recommend this approach in a production scenario.

## Dynamic Approach Using GTM SS

A better way to do this is to use Google Tag Manager (GTM SS) to add a custom event parameter to the GA4 events, indicating whether or not they are conversion events. In this case, we use GA4's tracking library (gtag.js) to flag conversion events with the query parameter `&_c=1` automatically. This parameter is present only for conversion events. It is furthermore exposed in GTM SS's event data in the `x-ga-systems_properties` and will be `true` for any conversion event. We can access this parameter in GTM SS using a custom event data variable, like so:

![event-data-variable](/assets/img/ga4-conversions-to-bq/event-data-variable.png)
_Exemplary Event Data Variable - Own GTM SS Setup_

We can then enrich the GA4 tag in GTM SS with a custom event parameter indicating whether or not the event is a conversion event, like so:

![ga4-tag-enriched](/assets/img/ga4-conversions-to-bq/ga4-tag-enriched.png)
_Exemplary Enriched GA4 Event Tag - Own GTM SS Setup_

For our SQL queries we can incorporate this custom event parameter by e.g. filtering for events where the custom event parameter is `true`.

The ability to enrich, redact, and modify the GA4 events in GTM SS amazes me every time I use it. It's such a powerful tool, especially since we lost Universal Analytics `customTask` feature with the advent of GA4 and the ability to modify GA4 events in the browser before they are sent. GTM SS is a great way to fill this gap.

The proposed setup doesn't require much work or maintenance, and it ensures that whatever conversions are configured in the GA4 UI will be directly available in BQ. This approach even takes care of the variable time component of conversion specifications, as the events will only be flagged as conversions if they are configured as such at the time of the event occurence. Although this approach requires GTM SS, but if you're already using GTM SS, this is a no-brainer. Setting up GTM SS for this purpose might be a massive overkill, though.

## Dynamic Approach Using GA4 Admin API and GCP

Therefore, I developed another dynamic approach. Here, I use the [GA4 Admin API](https://developers.google.com/analytics/devguides/config/admin/v1) and two more Google Cloud Platform (GCP) services to get the conversion metadata into BQ. It involves using the GA4 Admin API to fetch the conversion events and their properties and then uploading them to BQ via Cloud Functions, which can be repeatedly triggered with Cloud Scheduler. While the initial setup is a tad more complex than the previous approach, it's the most flexible and versatile I could come up with.

> Info: The **GA4 Admin API** allows you to manage GA4 properties and their resources programmatically and Google is still adding new features to it. The API is free to use and has a generous quota, that should be sufficient for most use cases.

### The Setup in GCP

For starters, we configure a Cloud Function that utilizes the GA4 Admin API's [properties.conversionEvents.list()](https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1beta/properties.conversionEvents/list) method to fetch the conversion metadata for a given GA4 property:

```python
def get_ga4_conversions(property_id, conversion_results):

    today = datetime.date.today().strftime('%Y-%m-%d')

    ga4_resp = ga4_client.list_conversion_events(parent=f"properties/{property_id}")
    for conversion_event in ga4_resp:
        conversion_results.append(
            {
                "date": today,
                "property_id": property_id,
                "conversion_api_name": conversion_event.name,
                "event_name": conversion_event.event_name,
                "create_time": conversion_event.create_time.isoformat(),
                "counting_method": conversion_event.counting_method.name,
            }
        )
    return conversion_results
```

> Info: **Cloud Functions** are a serverless execution environment for building and connecting cloud services. With Cloud Functions, you write simple, single-purpose functions that are attached to events emitted from your cloud infrastructure and services. Your Cloud Function is triggered when an event being watched is fired. Your code executes in a fully managed environment. There is no need to provision any infrastructure or worry about managing any servers.

The Cloud Function then formats the conversion metadata into a JSON format that we see fit and uploads it to BQ using the `bigquery.Client.load_table_from_json` method:

```python
def bq_upload(data):
    success = False
    # Check for table and create if it doesn't exist
    print(data)
    try:
        table = bq_client.get_table(TABLE_ID)
    except:
        table = bigquery.Table(TABLE_ID, schema=bq_schema)
        bq_client.create_table(table)
        time.sleep(10)

    # Upload data
    job_config = bigquery.LoadJobConfig(
        schema=bq_schema,
        write_disposition="WRITE_APPEND",
    )
    job = bq_client.load_table_from_json(data, TABLE_ID, job_config=job_config)
    job.result()
    print("Uploaded {} rows to {}.".format(job.output_rows, TABLE_ID))

    success = True

    return success
```

The resulting dataset will contain the following columns:

- `date`(DATE) - The date of the Cloud Function execution.
- `property_id`(STRING) - The GA4 property ID.
- `conversion_api_name`(STRING) - The API name of the conversion.
- `event_name`(STRING) - The event name of the conversion.
- `custom_event`(BOOL) - Whether the conversion is a custom event (e.g., for `purchase` it's `false`).
- `deletable`(BOOL) - Whether the conversion is deletable.
- `create_time`(TIMESTAMP) - The time the conversion was created.
- `counting_method`(STRING) - The counting method of the conversion.
- `default_conversion_value`(FLOAT) - The default conversion value.
- `default_conversion_value_currency_code`(STRING) - The currency code of the default conversion value.

> Info: **BigQuery** is a fully managed, serverless data warehouse that enables scalable analysis over petabytes of data, which supports querying using SQL. BQ is a powerful tool for data analysis and reporting.

You can find the full code for the Cloud Function [here](https://github.com/GunnarGriese/ga4-conversions-to-bq/blob/master/main.py) as well as detailed instructions on how to set it up in your environment. The Cloud Function can be triggered by a time-driven trigger to fetch the conversion events and upload them to BQ. I chose to use GCP's Cloud Scheduler to execute the Cloud Function in regular intervals.

![cloud-scheduler-config](/assets/img/ga4-conversions-to-bq/cloud-scheduler-config.png)
_Cloud Scheduler - Example Setup_

> Info: **Cloud Scheduler** is a fully managed enterprise-grade cron job scheduler. It allows you to schedule virtually any cloud infrastructure operation. You can use it to automate your infrastructure, saving time, reducing human error, and reducing costs.

That way, we can always ensure that we have the most recent conversion metadata in BQ. It is worth noting that the code above will append the recent conversion data to the table each time it is run. That way, we can keep track of the conversion metadata over time and even adjust our SQL queries to use it only for the date range for which it is valid.

The cost implications of this approach are minimal. The Cloud Function is executed only when triggered by the Cloud Scheduler, and the GA4 Admin API is free. The only cost to consider is the cost of storing the conversion metadata in BQ, which is negligible.

> DISCLAIMER: A similar mechanism could be built using [**Google Apps Script**](https://www.google.com/script/start/) together with Google Sheets. In that case, the App Script takes on the role of the Cloud Functions and would be triggered by a time-driven trigger to fetch the conversion events from the GA4 Admin API and upload them to the connected Google Sheet. I prefer the Python approach because it's more flexible, but if you need some (non-technical) user input, e.g., to add or remove conversion events, the Google Apps Script approach might be the better choice.

### Usage of Conversion Metadata in BigQuery

Now that we have the conversion metadata in BQ, we can join the GA4 raw data with the conversion events. Given the rich metadata we exported before, we can now incorporate a lot of different metrics into our SQL queries (e.g., conversion value, eligible period, etc.). All of these are helpful to build reports similar to the GA4 UI.

One of the most relevant data points obtained from the API is probably the respective [counting method](https://support.google.com/analytics/answer/13366706?hl=en) for a given conversion event. The counting method can be `ONCE_PER_EVENT` or `ONCE_PER_SESSION` and specifies if each time it occurs or is counted only once per session (like Universal Analytics goals). This differentiation should obviously be represented in the SQL query to give results matching the UI. Here's an example of how to do this using the newly obtained conversion metadata:

```sql
CREATE TEMP FUNCTION ga4EventParams(
-- s. full code here: https://zielinsky.alejand.ro/using-ga4-event-parameters-as-a-custom-dimensions-in-bigquery-f60978527fd)
);

WITH conversions AS ( --
    SELECT
        DISTINCT event_name,
        counting_method
    FROM
        `nlp-api-test-260216.analytics_conversions.ga4_conversions`
    WHERE
        property_id = '250400352'
),

session_info AS ( -- calculate session-level conversions
    SELECT
        user_pseudo_id,
        ga4EventParams('ga_session_id', event_params).value AS session_id,
        EXTRACT(
            DATE
            FROM
                TIMESTAMP_MICROS(event_timestamp) AT TIME ZONE "Europe/Copenhagen"
        ) AS day,
        COUNTIF(event_name IN (SELECT event_name FROM conversions WHERE counting_method = 'ONCE_PER_SESSION')) > 0 AS has_session_conversion
    FROM
        `nlp-api-test-260216.analytics_250400352.events_20240204`
    GROUP BY
        user_pseudo_id,
        session_id,
        day
)
SELECT
    day,
    COUNT(DISTINCT s.user_pseudo_id) AS users,
    COUNT(DISTINCT CONCAT(s.user_pseudo_id, session_id)) AS sessions,
    COUNTIF(event_name = 'page_view') AS page_views,
    COUNTIF(event_name IN (SELECT event_name FROM conversions WHERE counting_method = 'ONCE_PER_EVENT')) AS conversions, -- calculate event-level conversions
    SUM(IF(has_session_conversion, 1, 0)) AS session_conversions,
    COUNT(*) AS total_events
FROM
    session_info as s -- join event- and session-level conversions
    JOIN `nlp-api-test-260216.analytics_250400352.events_20240204` as e ON CONCAT(s.user_pseudo_id, session_id) = CONCAT(e.user_pseudo_id, ga4EventParams('ga_session_id', event_params).value)
GROUP BY
    day
ORDER BY
    day ASC;
```

The query above could be extended to include multiple properties, eligible periods for conversions, and conversion values. There's plenty of possibilities here. If you come up with something cool, let me know!

While this last approach requires more development effort and maintenance than the previous ones, the benefits are high. With the GA4 Admin API and GCP, we get the complete context of the conversion events and can use this information to build comprehensive reports in BQ, which we can expose to our dashboarding tool of choice.

You can find the complete code as well as detailed deployment instructions for the GCP infrastructure [here](https://github.com/GunnarGriese/ga4-conversions-to-bq/).

## Conclusion

The need for these workarounds stems from many companies trying to replicate the GA4 UI in BQ. At the same time, the BQ schema is not designed to be a 1:1 copy of the GA4 UI. Luckily, with the API-first approach of GA4, GTM SS's flexibility to easily manipulate GA4 events in real-time, or the (almost) unlimited possibilities of GCP, we can build a comprehensive reporting environment in BQ that is tailored to our needs.

To summarize the reviewed approaches, the manual approach is the most straightforward way to get the conversion events into BQ. However, there are better choices for fast-changing environments where the analyst does not fully control the data collection. The second approach, using GTM SS, is a good way to get the conversion events into BQ if you already use GTM SS. However, setting up GTM SS for this purpose is too much.

The GA4 Admin API and GCP approach is the best way to get the conversion events into BQ. This approach is the most flexible. It's also the most reliable way to get the conversion events into BQ, but it comes at the cost of some development effort and maintenance (which should be minimal).

I hope this post was helpful to you. If you have any questions or feedback, feel free to contact me.

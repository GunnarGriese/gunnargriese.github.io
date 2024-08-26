---
title: Who are my website users? And if so how many? - User IDs & Reporting Identities in GA4
author: gunnar
date: 2024-09-01 00:00:01 +0200
categories: [GA4]
tags: [ga4]
comments: true
---

Google Analytics 4 (GA4) can unify your users’ journeys using various methods, like User ID, Device ID, and Modeling. These methods allow GA4 to create a single user journey from all the event data associated with the same identity, visualizing it in the interface without any further setup. This enables a more unified, holistic history of users' interactions with your business and eventually allows you to report on user and session counts as well as associated metrics.

This blog post provides an overview of the Reporting Identity functionality with a special focus on logged in users, its quirks in GA4, its usage for your business, and its implications for reporting. Eventually, I will try to help you answer the (somewhat philisophical) question: "Who are my website users? And if so how many?"

## What is the Reporting Identity in GA4?

I know you're eager to cut to the chase, and I hate to hold you off, but before we can dive deeper into the topic, we have to establish some common ground and get the definitions straight:

1. The identifiers GA4 uses to unify a user's journey are collectively referred to as **identity spaces**.
2. The identity space(s) used by your GA4 property is called its **reporting identity**.

In the following sections you’ll find a description of each of the available identity spaces.

### User ID - Get to truly know your customers

If you create your own persistent IDs for signed-in users (e.g., CRM IDs), you can use these IDs to **measure user journeys across devices**. This requires consistently assigning IDs to your users and including the IDs along with the data you send to GA4 whenever they are browsing your website while logged in. The user ID is the most accurate and robust identity space because it uses data from self-authenticated users that you then collect to identify your users. Since these identifiers are the most stable and long-lasting identifiers and can especially be used for activation use cases, having a login functionality and nudging your users to use it is of great value for your business.

> The user IDs that you establish must adhere to GA4’s Terms of Service. This necessitates that you transparently communicate to your users the manner in which identifiers are utilized, as outlined in your Privacy Policy. Furthermore, the ID you assign should not encompass information that could potentially enable a third party to ascertain the identity of an individual user, such as an email address.

### Google Signals - Google’s data about your users

Google Signals is data from **users signed in to their Google account on their Chrome browser or Android device**. When Google Signals data is available, GA4 associates event data it collects from users with the Google accounts of signed-in users who have consented to share this information ([ads personalization consent is given in Google account settings](https://myadcenter.google.com/personalizationoff?sasb=true&ref=ad-settings)).

**Google stopped using Google Signals as an identity space in February 2024**, as it came with the significant drawback that its usage resulted in data points being withheld from the GA4 user interface, reducing the tool’s value for actual analytics work. We have decided to include it here anyway because, in the past, it has been a heavily debated identity space.

### User-Provided Data - 3rd-party cookie alternative

One of the most recently added functionalities in GA4 is "User-provided data collection". This allows you to send "consented, first-party data from your website to Google Analytics" (s. [here](https://support.google.com/analytics/answer/14077171?hl=en)). Google allows for hashed email addresses, phone numbers, names, and addresses to be sent to their platform. The data you send is then matched with other Google data (primarily browser data from logged-in Chrome users) to improve the accuracy of your measurement data and power capabilities like Enhanced Conversions and Demographics and Interests. I like to think of this method as replacing Google Signals for when Google will eventually phase out 3rd-party cookies - but on steroids.

Implementing the User-ID feature may not be possible for some websites (e.g., if your website doesn't have a login section). But for other websites, especially e-commerce sites, Google recommends that you set up the User-ID feature along with user-provided data collection to provide the most accurate user reporting in Analytics.

Interestingly enough, Google states in their documentation the following:

> "If you send user-provided data without also sending user IDs, collected user-provided data will be pseudonymized and used to **recognize unique users for user deduplication and reporting purposes.** When multiple types of user-provided data are provided, Analytics will prioritize them in the following order: email, phone, name, and address. Note that if user IDs are later provided for previously measured users with only user-provided data (no user ID), Analytics will **recognize these as separate users for reporting purposes.**" (s. [here](https://support.google.com/analytics/answer/14077171?hl=en))

So, although it's not part of the officially listed reporting identities, user-provided data appears to be used for user deduplication and reporting purposes, rendering it a _de facto identity space_. Since it’s quite a new feature, I am currently working together with my clients on understanding this feature even better, but have added it to this overview already.

### Device ID - Good ol’ cookies

GA4 can also use the device ID (also known as client ID or user pseudo ID) as an identity space. The device ID method is the least accurate because it only recognizes a device as the name suggests (not a user). At the same time, it is likely the most widely used method to identify users, as almost all analytics tools out there use it.

Coming back to the device ID, though:

- **For apps**: This is set to the App-Instance ID, which is unique to each app instance downloaded on a device.
- **For websites**: This is set by first-party cookies (`_ga` cookie for JS-managed or `FPID` cookie for GTM Server Side-managed cookies). You can inspect a user’s cookie ID in the "User Explorer" report, but be aware that it is called "Effective user ID" regardless if it was collected from a website or mobile app.

### Behavioural Modelling - The black box

When users decline GA4 identifiers like cookies, behavioural data for those users is unavailable. GA4 fills this gap by using the data of users who do accept cookies from the same property to model the behaviour of the users who decline cookies. For modelling to be working, the website needs to have Google Consent Mode implemented and the associated GA4 property [needs to have sufficient data](https://support.google.com/analytics/answer/11161109?hl=en#:~:text=and%20customer%20behavior.-,Prerequisites,-Because%20the%20model) to be eligible for behavioural modelling.

### Reporting Identity Options in GA4

In your GA4's property settings, you decide which identity spaces you want to use. The options in your settings then determine which of the available identity spaces GA4 will take into account if you make the required data available to GA4. The setting options are:

- **Blended**: Uses the User-ID, Device ID, then Modelling, in that order of preference.
- **Observed**: It uses the User-ID, Google Signals, and then Device ID, ignoring Modelling.
- **Device-based**: Only the device ID is used, and all other collected IDs are ignored.

So, we could say that GA4 is a user-centric analytics tool (not necessarily an end user-centric one though), as it always tries to use the User ID first, then the Device ID, and only then the Modelling data.

![Usage of reporting identies in GA4](/assets/img/ga4-reporting-identity/ga4-identity-spaces-order.png)
_Usage of identity spaces for Blended & Observed reporting identity_

**Adjusting the Reporting Identity** for a GA4 property requires you to navigate to the **Admin section**, select the correct account and property, click on Reporting Identity in the Property column, select the Reporting Identity you want to use, and click _Save_.
The reporting identity option you choose does **not** affect data collection or processing. Hence, you can switch between the options at any time without making any permanent impact on data. This is pretty neat, as you can directly assess within the interface what the impact on different identity spaces is on your data. Be aware that in order to get the full benefit of the Blended and Observed Reporting Identity, you need to collect user IDs.

![Available reporting identies in GA4](/assets/img/ga4-reporting-identity/ga4-available-reporting-identities.png)
_Available Reporting Identities in GA4_

## Implementation of Identity Spaces

So far, so good. Now, let’s get a tad more hands-on and have a look at how to implement the different identity spaces to unlock them for your reporting in GA4.

### User ID - Take advantage of the dataLayer

To enable the User ID as an identity space for GA4, a user’s internal ID needs to be actively sent to the analytics platform. For the GA4 tags in GTM being able to pick up the user ID, your developers will usually expose the user ID to the dataLayer whenever a user initially logs in. A respective dataLayer object could be structured as follows and sent with the `dataLayer.push()` method:

```javascript
window.dataLayer.push({
  event: "login",
  // other event data
  user: {
    id: "76588c85-b7a5-4967-9de7-695788e7a6f6",
    // other user data
  },
  status: "success",
});
```

From the moment on that a user has logged in, it is crucial that we enrich all GA4 events with the user’s ID. Therefore, we also need the developers to expose the ID on all of the following pages as early as possible, e.g., on `page_view` events.

```javascript
window.dataLayer.push({
  event: "page_view",
  // other event data
  user: {
    id: "76588c85-b7a5-4967-9de7-695788e7a6f6",
    // other user data
  },
});
```

If the value of the user ID key is populated, it can be read and "picked up" by a dataLayer variable in GTM.

![user-id-datalayer-vairable](/assets/img/ga4-reporting-identity/gtm-user-id-dlv.png)
_Exemplary GTM dataLayer variable for the user id key_

The value of the dataLayer variable is then included in all GA4 events as the value for the `user_id` field and sent with every outgoing GA4 request (`uid` query parameter).

![User ID in GA4 settings variable](/assets/img/ga4-reporting-identity/gtm-user-id-settings-variable.png)
_Exemplary GA4 settings variable for the user id key_

The variable above should then be associated with all GA4 tags. That way, we ensure that if the user ID is available in the dataLayer, we send it to GA4 - allowing for it to be used as an identity space.

> **Important**: I advise you to actually use the `user_id` field in your GA4 tags, as it is the field that GA4 expects to receive the user ID in. If you use a user property or event parameter to store the user ID (e.g., for analysis purposes or custom joins) and register these as a custom dimension in the interface, you [risk introducing a high-cardinality dimension](https://support.google.com/analytics/answer/14240153?sjid=14128691986949363561-EU&visit_id=638600919631579779-1410746499&rd=1#best-practices) that can lead to you seeing the `(other)` row in your reports.

### Device-based - Cookies for the masses

As mentioned above, cookies are the "default" method to identify users in analytics tools like GA4.

In a standard client-side measurement scenario, firing a Google or GA4 tag will result in the `_ga` cookie being placed in the user’s browser via the JavaScript `document.cookie` API. The cookie’s value is what GA4 titles the user’s device ID. The gtag.js tracking library then reads and updates the cookie value as specified in the script and attaches the value to all outgoing network requests to the GA4 servers (`cid` query parameter). GA4 uses the device ID to connect the event data points into a coherent user profile on which you can eventually report.

![GA4 client settings FPID cookie](/assets/img/ga4-reporting-identity/gtm-ss-fpid-cookie.png)
_GA4 client settings to manage FPID cookies_

If you add GTM Server-Side (GTM SS) to your measurement stack, you can [gain even more control](https://gunnargriese.com/posts/gtm-server-side/) over the cookie that determines your users’ Device IDs. In your GTM SS container, you’ll find that the standard GA4 client comes with additional configuration possibilities for _Cookies and Client Identification_. The client allows you to use your "own" first-party HTTP cookies (default name is `FPID`) to store the device ID. If you now route your GA4 requests through GTM SS and use the GA4 client to parse the event data, your GA4 tags will use the device ID stored in the FPID cookie instead of the one from the `_ga` cookie.

In the current digital landscape, which includes browser tracking prevention and ad blockers, cookies are often considered one of the less reliable user identifiers. They are easily deleted or expired, leading to potential overcounting of "users" on our website. However, they remain the primary identifier for the majority of our website users. While we can exert more control over cookies, overcoming the limitations of the technology itself is a complex task. So, should you embark on this journey to improve the reliability of your device ID, make sure you have a good reason (and a business case) to do so.

### Modelling - Let Google handle it

To unlock the _Modelling_ identity space you must leverage an Advanced Consent Mode implementation. In short, this means that you will execute your GA4 tags regardless of the users’ consent choices (e.g., no blocking of tags in case of missing consent). Additionally, you must ensure that you have Google’s Consent Mode correctly installed on your website or in your app to control the tags’ (cookie setting) behavior based on the users’ consent decisions.

Once Consent Mode is correctly installed on your website, GA4 tags will function as usual for consent users. In contrast, in the case of missing consent, the GA4 tags will send only so-called cookieless pings to GA4 servers without placing cookies in the users’ browsers. Using machine learning, Google will derive patterns from the consented or observed users and apply them to the unconsented or unobserved users, modeling their user journeys and derived metrics. Google phrases the process as Behavioral Modeling, which eventually allows insights into your website users' behavior and not only the consented subset.

> One interesting side fact is that the User ID will be available in the BigQuery raw data export, even if the user denies cookie consent and GA4 collects only "cookieless pings".

Since Consent Mode and its implementation are vast subjects with quite a few nitty-gritty details, I’d like to refer you to [my in-depth guide](https://gunnargriese.com/posts/consent-mode-v2/), which I published earlier this year. I’m sure it will serve you well in navigating that topic!

## Identity Space Implications on Reporting

Depending on which Reporting Identity you choose in your GA4 settings, the data you see in the GA4 interface will be different. The selected Reporting Identity influences how GA4 associates events with users and sessions, affecting the way GA4 reports on user and session counts and associated metrics. In the following paragraphs, I will focus on the implications related to the _User ID_ and _Modelling_ identity space since these require special attention (and are somewhat out of the ordinary).

### User ID in the GA4 interface

Let's prioritize the User ID, as it is the most powerful identifier in GA4 and should be treated equally in this blog post. So, here it goes!

#### Retroactive User ID Attribution

Suppose a user initially accesses a website without being logged in and logging in mid-session, transmitting a User ID during later events. In that case, GA4 uses the "User Pseudo ID" / client ID and the session ID to associate that session and all its events with the user ID provided when the user signs in.

![Retroactive User ID attribution in GA4](/assets/img/ga4-reporting-identity/ga4-retroactive-user-id-attribution.png)

In the example above, the User Explorer report will only display one "Effective User ID" (the User ID) set to `abc-567` for both events if _Blended_ or _Observed_ are used as the Reporting Identity. Suppose the _Device-based_ Reporting Identity has been chosen. In that case, the User Explorer report will only display one "Effective User ID" (the User Pseudo ID) set to `123.456` for both events. Furthermore, GA4 will report only one session for the two events, regardless of the Reporting Identity chosen.

![User ID in User Explorer report in GA4](/assets/img/ga4-reporting-identity/ga4-user-explorer.png)
_Retroactive User ID Attribution in BQ raw data, User Explorer, and Traffic Acquisition Report_

The screenshots above show how a mid-session login affects the raw data and the reporting in the User Interface (UI). While on the event level in the raw data, the `user_id` column is only populated from the time it's been collected, we can see (e.g., based on the event count) that it's being retroactively applied in the UI. Hence, it allows us to report on the "true" user journey and their associated sessions in the UI.

I consider this a pretty cool feature of GA4, especially since it is seamlessly integrated into the UI and doesn't require any additional effort to use.

#### What about proactive User ID Attribution?

A limitation of the User ID is that if GA4 detects subsequent events without the User ID set for the same User Pseudo ID, these will not be attributed to the User ID. So, once a user signs out and the `uid` parameter is no longer associated with the events, GA4 stops associating subsequent events with that user ID. See the visual below for a better understanding.

![Proactive User ID attribution in GA4](/assets/img/ga4-reporting-identity/user-id-proactive.png)
_Retroactive User ID Attribution Limitations_

In the scenario above, the User Explorer report in GA4 will display two distinct Effective User IDs, signifying two users: `123.456` (cookie ID) and `abc-567` (user ID).

As we have seen earlier, the initial three events will be associated with the `user_id`. Event number 4 will then be assigned to the cookie ID `123.456` only—and not the `user_id`. Additionally, it will also come with its own session. This behavior might "inflate" the user and session count in your reports, as the same user is counted twice.

Proactive user ID attribution does not exist in GA4, although it would be easy to implement from a technical perspective. This also means that it is of the utmost importance to ensure that the `user_id` field is populated when a deterministic identifier is available. Otherwise, your reports will contain fragmented user journeys and sessions.

#### Distinguish between signed-in and non-signed-in users

When you enable the User ID feature, you can compare _signed-in_ and _non-signed-in_ users in GA4. This is especially useful when you want to understand the behavior of users signed in to your website or app versus those not signed in. Below you can see a comparison between signed-in and non-signed-in users in GA4 utilizing GA4's _Comparison_ feature in combination with the dimension `Signed in with User ID`. This allows us to easily distinguish between these two groups of users.

![Signed in vs. non-signed in users in GA4](/assets/img/ga4-reporting-identity/ga4-signed-in-vs-not-signed-in.png)
_Comparison between signed-in and non-signed-in users in GA4_

> (Please ignore the high _Unassigned_ traffic share. I am still fine-tuning my synthetic user generator. 🧪🤖)

#### Replication of User ID in BigQuery

When you export your GA4 data to BigQuery, you will notice that both the `user_id` and the `user_pseudo_id` columns are available for analysis. Most likely, though, the `user_id` column will not be populated for most of your users. The `user_id` field is only populated when the User ID is collected. If the User ID is not collected, the `user_id` field will contain a `NULL` value, while GA4 will always populate the `user_pseudo_id` field with the Device ID. This is important to remember when you are querying your GA4 data in BigQuery and trying to match it to the interface.

If you seek to replicate the interface's reports in BigQuery, you can use the following query to calculate the effective user ID and session ID based on the `user_id` and `user_pseudo_id` fields. This query will allow you to see the same user journey in BigQuery as you would see in the GA4 interface - taking into account retroactive User ID association as outlined above.

```sql
-- Add temporary function to easily access ga4EventParams
SELECT
  event_timestamp,
  event_name,
  user_id,
  user_pseudo_id,
  COALESCE( FIRST_VALUE(user_id IGNORE NULLS) OVER (PARTITION BY CONCAT(user_pseudo_id, ga4EventParams('ga_session_id', event_params).value)
    ORDER BY
      event_timestamp ROWS BETWEEN CURRENT ROW
      AND UNBOUNDED FOLLOWING), user_pseudo_id) AS effective_user_id,
  ga4EventParams('ga_session_id',
    event_params).value AS raw_session_id,
  CONCAT( COALESCE( FIRST_VALUE(user_id IGNORE NULLS) OVER (PARTITION BY CONCAT(user_pseudo_id, ga4EventParams('ga_session_id', event_params).value)
      ORDER BY
        event_timestamp ROWS BETWEEN CURRENT ROW
        AND UNBOUNDED FOLLOWING), user_pseudo_id ), ga4EventParams('ga_session_id',
      event_params).value ) AS effective_session_id
FROM
  `<your-project-id>.analytics_<your-property-id>.events_*`
WHERE
  _TABLE_SUFFIX BETWEEN '<your-start-date>'
  AND '<your-end-date>'
  AND user_pseudo_id = '2030451950.1721832151' -- select a specific user for testing
ORDER BY
  event_timestamp ASC
```

The `effective_user_id` is calculated using a window function that partitions the data by a combination of `user_pseudo_id` and `session_id`. The `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` ensures that the `FIRST_VALUE` window function captures the first non-null `user_id` from the current row onward within the partition. This logic stops populating `effective_user_id` with the `user_id` once the user logs out because, after the logout event, the subsequent rows no longer have a valid `user_id` within the remaining partition, causing the `COALESCE` function to revert to `user_pseudo_id`, effectively resetting the default cookie-based identifier for the rest of the session. You can inspect the result of the query in the screenshot below to see how the query effectively resolves the available identity spaces:

![Calculate effective user and session id in BigQuery](/assets/img/ga4-reporting-identity/ga4-bq-effective-user-session-id.png)
_Calculate effective user and session id in BigQuery for User IDs_

### (Behavioral) Modeling in the GA4 interface

When enabling the Behavioral Modeling identity space, GA4 will use their proprietary Machine Learning algorithm to model the behavior of users who have not consented to cookies (but for which you collect cookieless pings) based on the behavior of users who have consented to cookies. This means that the user journey data you see in the GA4 interface for these users is not the actual data but a model of the data. While the model is quite accurate from my experiences and tests, it is essential to remember that it is an estimate - not more, not less.

![Behavioral Modeling in GA4](/assets/img/ga4-reporting-identity/behavioral-modeling-data-quality-card.png)

Luckily, GA4 provides you with a **data-quality icon** that indicates whether the data you are looking at is modeled and, if so, when the _Modeling_ identity space was unlocked. This is especially helpful when you include date ranges in your analysis when the Modeling identity space has yet to be enabled. So, while it is a good feature to help you assess high-level trends, like overall user and session counts, you should always take the results with a grain of salt.

## Advanced Use Cases for User IDs in GA4

As mentioned before, the User ID identity space is the most beneficial one. Not only because it is the most accurate and robust identity space but mainly because it sets you up with a solid foundation for more advanced use cases. Namely, enriching your website and app data with CRM or other data from other business-relevant applications and using it to build meaningful audiences. You can use the User ID to create more personalized experiences for users. For example, you can use the User ID to link a user's behavior on your website or app to their profile in your CRM system, allowing you to tweak their experience based on their past behavior.

Let's have a look at the various methods for using first-party data in GA4.

### Using the Measurement Protocol

The Measurement Protocol (MP) is a method for sending data to GA4 server-to-server. Accordingly, it allows you to send data to GA4 from any internet-connected device, such as a CRM. This method is especially useful for augmenting your GA4 data with data points unavailable client-side—exactly what we need for our User ID use case.

To send data to GA4 using the MP, you need to send a POST request from our system to the GA4 endpoint with the required parameters. The following example shows how to send a user property along with an event:

```javascript
const measurementId = "<your-stream-id>";
const apiSecret = "<your-api-secret-value>";

// Function to request a user's customer score from the CRM.
const customerScore = getCustomerScore(userId);

const queryParams = `?measurement_id=${measurementId}&api_secret=${apiSecret}`;
fetch(`https://www.google-analytics.com/mp/collect${queryParams}`, {
  method: "POST",
  body: JSON.stringify({
    user_id: userId, // The unique identifier for a user.
    user_properties: {
      customer_score: {
        value: customerScore, // The user's customer score.
      },
    },
    events: [
      {
        name: "customer_score_enrichment", // The event name.
      },
    ],
  }),
});
```

In the snippet above, we "fetch" a customer score for a given User ID from our CRM system and send it to GA4 using the Measurement Protocol. The request includes the User ID, the user property `customer_score`, and an event named `customer_score_enrichment`.

> Note: The sample above showcases how to send a user property along with an event, but sending a request that only contains user properties works just as fine.

While the MP is a powerful tool, it can be challenging to fine-tune as it is easy to inflate the session count or fail to attribute events correctly to their session source. Hence, it requires a bit more technical know-how to set up and maintain—it's a good idea to get your developers involved as well. If you want to learn more about the Measurement Protocol, I recommend checking out the [official documentation](https://developers.google.com/analytics/devguides/collection/protocol/ga4).

### Using GTM Server-Side and Firestore

To simplify the retrieval of first-party data, GTM Server-Side (GTM SS) comes with a _Firestore Lookup variable_, allowing you to pull values from specific keys or fields in a Firestore document to enrich data streams routed through GTM SS.

![gtm-ss-firestore](/assets/img/ga4-cdp/gtm-ss-firestore.png)
_GTM SS Firestore Variable_

In the context of this blog post, we want to use the Firestore Lookup variable to enrich GA4 data with the customer score from the MP example. Our lookup key in this case is the User ID and we use the Firestore Lookup variable to retrieve a user’s respective score from a Firestore document and then send it to GA4 via a server-side event. Obviously, this requires that you have set up a Firestore database and populate it frequently with the users' latest score values to ensure you feed GA4 with relevant data.

### Using GA4 Data Import

![ga4-data-import](/assets/img/ga4-reporting-identity/ga4-data-import.png)
_GA4 Data Import Interface_

Read more about GA4 Data Import based on User IDs in the [official documentation](https://support.google.com/analytics/answer/10071143?hl=en&ref_topic=10054560&sjid=5542917637782379063-EU#).

> Note: If you don't have a user ID available, GA4 also allows you perform the import based on the device ID. This comes in especially handy for lead generation websites or websites that don't have a login functionality.

Since these identifiers are the most stable and long-lasting identifiers and can especially be used for activation use cases, having a login functionality and nudging your users to use it is of great value for your business.
If you found this section interesting, I can recommend hoping over to my article [GA4 - the CDP You Didn't Know You Had](https://gunnargriese.com/posts/ga4-the-cdp-you-didnt-know-you-had/) for more food for thought.

## Conclusion

Phew - let's take a deep breath together! That was a lot of information to digest, but I hope I managed to convey it in a way that is easy to understand and follow. Furthermore, I hope you now better understand the Reporting Identity in GA4, its intricacies, and how to implement the different identity spaces.
Blending all the identities together into one overview makes it sometimes hard to see the true impact

If you have any questions or need further clarification, please don't hesitate to reach out to me. I am always happy to help!

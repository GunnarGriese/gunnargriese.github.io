---
title: Who are my users - The Reporting Identity in GA4
author: gunnar
date: 2024-09-01 00:00:01 +0200
categories: [GA4]
tags: [ga4]
comments: true
---

![gtm-ss-](/assets/img/ga4-data-quality/gtm-ss-architecture.png)
_Source: Own Visualization of a sGTM setup powered by GA4_

Google Analytics 4 (GA4) can unify your users’ journeys using various methods, like User ID, Device ID, and Modeling. These methods allow GA4 to create a single user journey from all the event data associated with the same identity, visualizing it in the interface without any further setup. This enables a more unified, holistic history of users' interactions with your business and eventually allows you to report on user and session counts as well as associated metrics.

This blog post provides an overview of the Reporting Identity functionality, its quirks in GA4, its usage for your business, and its implications for reporting.

## What is the Reporting Identity in GA4?

Before we dive into the topic too deeply, let’s establish some common ground and get the definitions straight. The identifiers GA4 uses to unify a user's journey are collectively referred to as **identity spaces**. The identity space(s) used by your Analytics property is called its **reporting identity**. In the following sections you’ll find a description of each of the available identity spaces.

![usage of reporting identies in GA4](/assets/img/ga4-reporting-identity/ga4-identity-spaces-order.png)
_Usage of identity spaces for Blended & Observed reporting identity_

### User ID - Get to truly know your customers

If you create your own persistent IDs for signed-in users (e.g., CRM IDs), you can use these IDs to **measure user journeys across devices**. This requires consistently assigning IDs to your users and including the IDs along with the data you send to GA4 whenever they are browsing your website while logged in. The user ID is the most accurate and robust identity space because it uses data from self-authenticated users that you then collect to identify your users. Since these identifiers are the most stable and long-lasting identifiers and can especially be used for activation use cases, having a login functionality and nudging your users to use it is of great value for your business.

> The user IDs that you establish must adhere to GA4’s Terms of Service. This necessitates that you transparently communicate to your users the manner in which identifiers are utilized, as outlined in your Privacy Policy. Furthermore, the ID you assign should not encompass information that could potentially enable a third party to ascertain the identity of an individual user, such as an email address.

### Google Signals - Google’s data about your users

Google Signals is data from **users signed in to their Google account on their Chrome browser or Android device**. When Google Signals data is available, GA4 associates event data it collects from users with the Google accounts of signed-in users who have consented to share this information ([ads personalization consent is given in Google account settings](https://myadcenter.google.com/personalizationoff?sasb=true&ref=ad-settings)).

**Google stopped using Google Signals as an identity space in February 2024**, as it came with the significant drawback that its usage resulted in data points being withheld from the GA4 user interface, reducing the tool’s value for actual analytics work. We have decided to include it here anyway because, in the past, it has been a heavily debated identity space.

### User-Provided Data - 3rd-party cookie alternative

One of the most recently added functionalities in GA4 is “User-provided data collection". This allows you to send “consented, first-party data from your website to Google Analytics" (s. [here](https://support.google.com/analytics/answer/14077171?hl=en)). Google allows for hashed email addresses, phone numbers, names, and addresses to be sent to their platform. The data you send is then matched with other Google data (primarily browser data from logged-in Chrome users) to improve the accuracy of your measurement data and power capabilities like Enhanced Conversions and Demographics and Interests. I like to think of this method as replacing Google Signals for when Google will eventually phase out 3rd-party cookies - but on steroids.

Implementing the User-ID feature may not be possible for some websites (e.g., if your website doesn't have a login section). But for other websites, especially e-commerce sites, Google recommends that you set up the User-ID feature along with user-provided data collection to provide the most accurate user reporting in Analytics.

Interestingly enough, Google states in their documentation the following:

> “If you send user-provided data without also sending user IDs, collected user-provided data will be pseudonymized and used to recognize unique users for user deduplication and reporting purposes. When multiple types of user-provided data are provided, Analytics will prioritize them in the following order: email, phone, name, and address. Note that if user IDs are later provided for previously measured users with only user-provided data (no user ID), Analytics will recognize these as separate users for reporting purposes.." (s. [here](https://support.google.com/analytics/answer/14077171?hl=en))

So, although it's not part of the officially listed reporting identities, user-provided data appears to be used for user deduplication and reporting purposes, rendering it a **de facto identity space**. Since it’s quite a new feature, I am currently working together with my clients on understanding this feature even better, but have added it to this overview already.

### Device ID - Good ol’ cookies

GA4 can also use the device ID (also known as client ID or user pseudo ID) as an identity space. The device ID method is the least accurate because it only recognizes a device as the name suggests (not a user). At the same time, it is likely the most widely used method to identify users, as almost all analytics tools use it.

Coming back to the device ID, though:

- **For apps**: This is set to the App-Instance ID, which is unique to each app instance downloaded on a device.
- **For websites**: This is set by first-party cookies (`_ga` cookie for JS-managed or `FPID` cookie for GTM Server Side-managed cookies). You can inspect a user’s cookie ID in the "User Explorer" report, but be aware that it is called "Effective user ID" regardless if it was collected from a website or mobile app.

### Behavioural Modelling - The black box

When users decline GA4 identifiers like cookies, behavioural data for those users is unavailable. GA4 fills this gap by using the data of similar users who do accept cookies from the same property to model the behaviour of the users who decline cookies. For modelling to be working, the website needs to have Google Consent Mode implemented and the associated GA4 property [needs to have sufficient data](https://support.google.com/analytics/answer/11161109?hl=en#:~:text=and%20customer%20behavior.-,Prerequisites,-Because%20the%20model) to be eligible for behavioural modelling.

### Reporting Identity Options in GA4

In your GA4's property settings, you decide which identity spaces you want to use. The options in your setting then determine which of the available identity spaces GA4 will take into account if you make the required data available to GA4. The setting options are:

- **Blended**: Uses the User-ID, Device ID, then Modelling, in that order of preference.
- **Observed**: It uses the User-ID, Google Signals, and then Device ID, ignoring Modelling.
- **Device-based**: Only the device ID is used, and all other collected IDs are ignored.

![Available reporting identies in GA4](/assets/img/ga4-reporting-identity/ga4-available-reporting-identities.png)
_Available Reporting Identities in GA4_

**Adjusting the Reporting Identity** for a GA4 property requires you to navigate to the **Admin section**, select the correct account and property, click on Reporting Identity in the Property column, select the Reporting Identity you want to use, and click _Save_.
The reporting identity option you choose does **not** affect data collection or processing. Hence, you can switch between the options at any time without making any permanent impact on data. This is pretty neat, as you can directly assess within the interface what the impact on different identity spaces is on your data. Be aware that in order to get the full benefit of the Blended and Observed Reporting Identity, you need to collect user IDs.

## Implementation of Identity Spaces

So far, so good. Now, let’s have a look at how to implement the different identity spaces to unlock them for your reporting in GA4.

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

### Device-based - Cookies for the masses

As mentioned above, cookies are the “default" method to identify users in analytics tools like GA4.

In a standard client-side measurement scenario, firing a Google or GA4 tag will result in the `_ga` cookie being placed in the user’s browser via the JavaScript `document.cookie` API. The cookie’s value is the user’s device ID. The gtag.js tracking library then reads and updates the cookie value as specified in the script and attaches the value to all outgoing network requests to the GA4 servers (`cid` query parameter). GA4 uses the device ID to connect the event data points into a coherent user profile on which you can eventually report.

![GA4 client settings FPID cookie](/assets/img/ga4-reporting-identity/gtm-ss-fpid-cookie.png)
_GA4 client settings to manage FPID cookies_

If you add GTM Server-Side (GTM SS) to your measurement stack, you can gain even more control over the cookie that determines your users’ Device IDs. In your GTM SS container, you’ll find that the standard GA4 client comes with additional configuration possibilities for _Cookies and Client Identification_. The client allows you to use your “own" first-party HTTP cookies (default name is `FPID`) to store the device ID. If you now route your GA4 requests through GTM SS and use the GA4 client to parse the event data, your GA4 tags will use the device ID stored in the FPID cookie instead of the one from the `_ga` cookie.

In the current digital landscape, which includes browser tracking prevention and ad blockers, cookies are often considered one of the less reliable user identifiers. They are easily deleted or expired, leading to potential overcounting of “users" on our website. However, they remain the primary identifier for the majority of our website users. While we can exert more control over cookies, overcoming the limitations of the technology itself is a complex task.

### Modelling - Let Google handle it

To unlock the _Modelling_ identity space you must leverage an Advanced Consent Mode implementation. In short, this means that you will execute your GA4 tags regardless of the users’ consent choices (e.g., no blocking of tags in case of missing consent). Additionally, you must ensure that you have Google’s Consent Mode correctly installed on your website or in your app to control the tags’ (cookie setting) behavior based on the users’ consent decisions.

Once Consent Mode is correctly installed on your website, GA4 tags will function as usual for consent users. In contrast, in the case of missing consent, the GA4 tags will send only so-called cookieless pings to GA4 servers without placing cookies in the users’ browsers. Using machine learning, Google will derive patterns from the consented or observed users and apply them to the unconsented or unobserved users, modeling their user journeys and derived metrics. Google phrases the process as Behavioral Modeling, which eventually allows insights into your website users' behavior and not only the consented subset.  
One interesting side fact is that the User ID will be available in the BigQuery raw data export, even if the user denies cookie consent and GA4 collects only "cookieless pings".

Since Consent Mode and its implementation are vast subjects with quite a few nitty-gritty details, I’d like to refer you to [my in-depth guide](https://gunnargriese.com/posts/consent-mode-v2/), which I published earlier this year. I’m sure it will serve you well!

## Implications on Reporting

### The Wonders of Retroactive User ID Attribution

Suppose a user initially accesses a website without being logged in and logging in mid-session, transmitting a User ID during later events. In that case, GA4 uses the "User Pseudo ID" / client ID and the session ID to associate that session and all its events with the user ID provided when the user signs in.

![Retroactive User ID attribution in GA4](/assets/img/ga4-reporting-identity/ga4-retroactive-user-id-attribution.png)

In the example above, the User Explorer report will only display one "Effective User ID" (which is the User ID) set to `abc-567` for both of these events if Blended or Observed are used as the Reporting Identity. If the Device-based Reporting Identity has been chosen, the User Explorer report will also only display one "Effective User ID" (which is the User Pseudo ID) set to `123.456` for both of these events.

![User ID in User Explorer report in GA4](/assets/img/ga4-reporting-identity/ga4-user-explorer.png)
_Retroactive User ID Attribution in BQ raw data, User Explorer, and Traffic Acquisition Report_

In the screenshots above, you can see how a mid-session login affects the raw data and the reporting in the User Interface (UI). While on event-level in the raw data, the user_id column is only populated from the time it's been collected, we can clearly see (e.g., based on the event count) that it's being retroactively applied in the UI. Hence, it allows us to report on the "true" users and their associated sessions in the UI.

### What about proactive User ID Attribution?

A limitation of the User ID is, if more events are detected by the same User Pseudo ID without the User ID set then these will not be attributed to the User ID. So, once a user signs out and the uid parameter is not associated with the events anymore, GA4 stops associating any subsequent events with that user ID.

![Proactive User ID attribution in GA4](/assets/img/ga4-reporting-identity/user-id-proactive.png)
_Retroactive User ID Attribution Limitations_

In the scenario above, the User Explorer report will display two distinct Effective User IDs, signifying two users: `123.456` (cookie ID) and `abc-567` (user ID).

As we have seen earlier, the initial three events will be associated with the `user_id`. The event number 4 will then be assigned to the cookie ID `123.456` only - and not the `user_id`.

Proactive user ID attribution does not exist in GA4, although it would be easy to implement from a technical perspective. At the same time, it makes sense from an analytics and privacy perspective that ...

![Benefits of using BigQuery with GA4](/assets/img/ga4-reporting-identity/ga4-bq-benefits.png)

WORK FROM HERE: https://docs.google.com/document/d/1NyZhY76iSPgUdtOKi9Xvz0qzOsh2f4Wz6KBBo2F2fj0/edit

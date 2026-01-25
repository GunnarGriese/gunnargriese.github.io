---
layout: post
title: GA4 Client-Side Data Redaction - How to remove PII from your data before you collect it
author: gunnar
date: 2023-09-26 06:21:15 +0200
categories: [GA4]
tags: [ga4]
image: /assets/images/blog/ga-data-redaction.png
comments: true
lang: en
permalink: /posts/ga4-data-redaction/
---

In my recent article, I explored the potential of GA4 as a core component in crafting a [lightweight Composable CDP](/posts/ga4-the-cdp-you-didnt-know-you-had/). One of the capabilities for a Composable CDP is its ability to account for Data Governance and Privacy Controls. Building on that, this post zooms in on GA4's capabilities that allow for data management in alignment with privacy standards. At the heart of our discussion is the Client-Side Data Redaction feature, designed to scrub out personally identifiable information (PII) before GA4's data collection ensues.

As outlined in Google Analytics' [Terms and Conditions](https://marketingplatform.google.com/about/analytics/terms/us/#:~:text=and%20security%20measures.-,7.%20Privacy.,-You%20will%20not), transmitting PII, be it names, email addresses, or even credit card numbers, is a strict no-no. Through this post, I'll walk you through the nuances of leveraging GA4's client-side data redaction, ensuring your data remains PII-free before reaching Google Analytics. Alongside, we'll also uncover the mechanics behind this feature and explore more methodologies to fortify your data against PII leaks to GA4.

## GA4 Data Collection under the Hood

Initially, let's dissect how GA4's data collection functions internally. The subsequent diagram illustrates the data collection pipeline of GA4 for a typical client-side measurement setup. This pipeline encompasses three phases:

1. Loading the tracking library (gtag.js) and the measurement logic, often through GTM.
2. Dispatching the intended events along with their metadata to GA4.
3. Processing data on GA4's servers, where data from users' browsers is gathered and aggregated.

![ga-data-pipeline](/assets/images/ga4-data-redaction/ga4-data-pipeline.png "GA4 Data Pipeline")
_GA4 Data Pipeline - Own Visualization_

Similar to Universal Analytics (UA), certain configurations of the platform are responsible for how data is processed before it is exposed to the analyst. For instance, for how long data is retained (Data Rentention) settings or how to reat certain traffic types (e.g., exclude it from the data set or mark it up via a dimension). Again, this just like in UA, where Property and View settings were responsible for how data is processed before it is exposed to the analyst.

A notable change in GA4 is Google's decision to relocate specific processing logic from its servers to the client-side. My hypothesis is that this transition was made to conserve computational resources — a reasonable shift, especially considering its free availability to most users.

This migration implies that the users' browsers, as part of the data collection phase, now take over some pre-transmission processing tasks. This encompasses areas like sessionization logic. Contrary to UA where sessionization was managed server-side, GA4 delegates this responsibility to the browser. Here, the browser discerns session commencements and terminations, storing session identifiers in cookies and transmitting them with events to GA4. The GA4 endpoint then uses these identifiers to classify events into new or existing sessions, bypassing the need for rolling windows in the processing pipeline. Also, other configurations like IP-based internal traffic detection, new feature implementations like event modification, and event marking as [conversions](/posts/ga4-conversions-to-bigquery/) now occur within browsers.

The analytics team, using the GA4 Admin panel, sets these configurations by defining the property and/or data stream settings. These configurations are then dispatched to users' browsers through the gtag.js library, either embedded directly or via the GA4 Configuration tag/Google tag through GTM. For UA, a universal tracking library (analytics.js) was in use. The JavaScript (JS) within was uniform for every UA user. In contrast, GA4's request to fetch the gtag.js library now carries the Data Stream's Measurement ID (`/gtag/js?id=G-XXXXXX`). This ensures that the gtag.js library aligns specifically with your GA4 property and data stream, a logical transition considering the aforementioned.

This paradigm shift, while presenting its own set of challenges, also allows us to get deeper insights into GA4's internal mechanics. For example, we can now dissect the gtag.js library to understand the functionality of the newly introduced **Client-Side Data Redaction** feature. This exploration will be the focus of our subsequent section.

## Client-Side Data Redaction in GA4

In Google Analytics 4 (GA4), we now have the flexibility to configure [Data Redaction](https://support.google.com/analytics/answer/13544947) specifically for Web Data Streams, focusing on predefined text patterns like **email addresses and URL query parameters**. This feature ["leaked"](https://www.linkedin.com/posts/charlesfarina_a-new-data-redaction-feature-just-rolled-activity-7087161324031414272-YaJG/) two months ago already, when Google's official GA4 demo property was granted access to the feature. However, it was only recently that the feature has become available to more and more GA4 users (it appears to be part of a gradual roll-out effort).

When it comes to email redaction, this feature **operates across the entire GA4 event** on a best-effort basis, ensuring a layer of privacy and security. On the other hand, URL Query Parameters specifically target a select set of event parameters for which GA4 will attempt to redact values of the specified query parameters. The URL query parameter redaction is currently supported for the following event parameters (all URL-related parameters):

- `page_location`
- `page_referrer`
- `page_path`
- `link_url`
- `video_url`
- `form_destination`

### How to enable Data Redaction in GA4

To enable Data Redaction, navigate to the Admin panel of your GA4 property and select the desired Web Data Stream. Here, you'll find the Data Redaction tab, where you can enable the feature and specify the parameters you'd like to redact. You can choose to redact email addresses and/or URL query parameters. For the latter, you can specify the parameters you'd like to redact. For instance, if you'd like to redact the `firstname` and `lastname` parameters, you can enter them in the text box, separated by commas.

Activating Client-Side Data Redaction in GA4 is straightforward. Simply follow these steps:

1. Access the Admin panel of your GA4 property.
2. Choose the Web Data Stream you wish to modify.
3. Locate the Data Redaction tab.
4. Here, you can activate the Data Redaction feature and delineate the specific parameters to redact.

![ga4-interface-data-redaction](/assets/images/ga4-data-redaction/ga4-interface-data-redaction.png "GA4 Data Redaction Interface")
_GA4 Data Redaction Interface_

Within the settings you'll also have the ability to preview the effect of the Data Redaction settings:

![ga4-interface-redact-preview](/assets/images/ga4-data-redaction/ga4-interface-redact-preview.png "GA4 Data Redaction Preview")
_GA4 Data Redaction Preview_

It's important to note, however, that this feature is exclusive to Web Data Streams and is not available for App Data Streams. Additionally, if you are using pre-existing Web Data Streams, both email and query parameter redaction features will be turned `OFF` by default. For newly created Web Data Streams, Email redaction will be enabled automatically, while Query Parameter redaction will remain `OFF`. This design provides a customizable approach to data handling, ensuring GA4 users can adeptly navigate between utility and privacy.

### Effect of Data Redaction on Data Collection

Let's have a look at how the Data Redaction feature affects data collection. To do so, we'll use the following example, where I have configured the Data Redaction feature to redact email addresses. I've also configured a GA4 Configuration tag in GTM to send a `page_view` event to GA4. The tag is configured to send the following values for some custom event parameters:

![gtm-test-values](/assets/images/ga4-data-redaction/gtm-test-values.png "GTM Data Redaction test")
_GTM Test Configuration_

As you can see, the values represent various combinations of email addresses and strings. The following table shows the values that are sent to GA4, along with the redacted values:

| Original Value                    | Redacted Value          |
| --------------------------------- | ----------------------- |
| testmail@gunnar.com               | (redacted)              |
| separate_str testmail@gunnar.com  | separate_str (redacted) |
| joined_strtestmail@gunnar.com     | (redacted)              |
| testmail@gunnar.comjoined_strtest | (redacted)\_strtest     |

The data redaction logic replaces email addresses with the string `(redacted)`. It's important to note that the redaction logic for email addresses is applied to the entire event and all of its parameters. For instance, an email address detected in the `search_term` parameter will be redacted, even if the `search_term` parameter is not specified in the Data Redaction settings. Search terms containing PII like email addresses is something I've seen very often, having a simple to configure "global" setting preventing is a nice addition. This scope does **not** apply for the URL query parameter redaction feature though. If you specify a query parameter to be redacted, the redaction logic will be applied to only the previously mentioned URL-related event parameters, even though they are not explicitly specified in the Data Redaction settings.

### Components of the Data Redaction Feature

Let's have a closer look at what Google means by "best-effort basis". As mentioned earlier, we can expect this logic to present in gtag.js and when searching my specific instance of the code, we indeed find the following part of the code that holds the specifications from my web data stream:

```json
{
  "function": "__ccd_auto_redact",
  "priority": 1,
  "vtp_redactEmail": true,
  "vtp_redactQueryParams": "zipcode,creditcarddetails,password,firstname,lastname",
  "vtp_instanceDestinationId": "G-XXXXXXXXXX",
  "tag_id": 12
}
```

Furthermore, we find two regular expressions (regex) in the gtag.js-file that appear to be linked to the data redaction feature:

- `[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}` (case insensitive)
- `[A-Z0-9._-]|%25|%2B)+%40[A-Z0-9.-]` (case insensitive)

Let's break down the regex to understand what it does:

- `[A-Z0-9._%+-]+`: This matches one or more occurrences (+) of uppercase letters (A-Z), digits (0-9), dots (.), underscores (\_), percent signs (%), plus (+), or hyphens (-). It corresponds to the "user" part of an email address (e.g., the john.doe in john.doe@example.com).
- `@`: This matches the "@" symbol, which is a required part of an email address.
- `[A-Z0-9.-]+`: This matches one or more occurrences (+) of uppercase letters (A-Z), digits (0-9), dots (.), or hyphens (-). It corresponds to the "domain" part of the email address (e.g., the example in john.doe@example.com).
- `\\.`: This matches a single dot (.). The backslashes are used to escape the dot, as it is a special character in regex.
- `[A-Z]{2,}`: This matches two or more occurrences ({2,}) of uppercase letters (A-Z). It corresponds to the "top-level domain" (e.g., com, org, net) part of an email address (e.g., the com in john.doe@example.com).

The purpose of this regular expression is to match email addresses that follow a specific pattern. It only matches email addresses that consist of letters, numbers, and certain special characters. It expects the top-level domain to have at least two characters. It also expects the email address to have a "user" part, an "@" symbol, a "domain" part, and a "top-level domain" part.

GA4's data redaction treats percent-encoded URL query parameters as well, including Unicode characters accepted by browsers. This is what the second regex is for. It's a variation of the first regex, but it matches percent-encoded characters. The percent-encoded characters are represented by the `%25` and `%2B` parts of the regex.

### Caveats

In terms of operation, Data Redaction kicks in **after** Event Modification & Creation. This means that any rules you've set to modify or create events will be executed on the website before the Data Redaction process starts. It's also important to be cautious, as there is a risk of unintended data redaction. For instance, certain parts of the URL or user configurations provided in tags could be mistakenly redacted if they resemble email addresses:

> Data redaction may incorrectly interpret text as an email address and redact the text; for example, if the text includes "@" followed by a top-level domain name (e.g., example.com) it may be incorrectly removed.

Historically, similar data manipulation could be achieved in your GTM web container by tweaking the `page_location` or leveraging GTM Server-Side (sGTM) transformations. Still, remember that sensitive parameters dispatched via HTTP headers, like IP addresses, referers, and user-agents, demand special attention and handling within sGTM.

While the Data Redaction feature in GA4 offers you greater control over the data collected, it's crucial to understand that this is not a one-size-fits-all solution for ensuring compliance with all laws and regulations. For a comprehensive understanding of best practices and controls for safeguarding data, I strongly recommend working together with your legal department.

Lastly, it's worth noting that this feature will not prevent data collection via other methods like Measurement Protocol (MP) or Data Import. Therefore, while Data Redaction is a useful tool, it should be part of a broader data management and compliance strategy.

## Other Privacy Controls in GA4

Hence, let's have a look at additional approaches that you can use to ensure that you do not send any PII to GA4.

### Regional Data Controls in GA4

While Client-Side Data Redaction is great to control what data is sent with the GA4 event, other metadata of the request to GA4, e.g. IP addresses and user-agents, might require further treatment as well. Furthermore, the usage of Google Signals might be something that you want use only under specific circumstances.

With GA4, you're empowered with **Regional Data Controls** that allow you to define the specificity of location and device data you collect from your website users. Opting to disable this collection ensures that city-level location insights (derived from IP addresses) and certain device metadata (dervied from user-agent headers) are redacted even before they reach GA4's servers. For a deep-dive into these controls, visit the official documentation on [Regional Controls & Google Signals](https://support.google.com/analytics/answer/12017362?hl=en#:~:text=analytics.google.com-,Regional%20controls,-Google%20signals).

Moreover, GA4 offers advanced configurations, both in gtag.js & GTM web containers, to fine-tune ad personalization and the usage of Google Signals: `allow_google_signals` & `allow_ad_personalization_signals`.

Within the Property Settings, you can harness these advanced configurations to either enable or disable ad personalization for users from specific countries or US states. It's important to note that these settings are forward-looking, meaning they won't alter previously collected data. Opting to turn off ad personalization doesn't inhibit your capability to use the analytics data from that property for other purposes, like A/B testing in tools like Optimizely, AB Tasty, etc. or Firebase.

Should you decide to disable ad personalization for any region, all events harvested from that area will be flagged as ineligible for ad personalization (NPA). This ensures that conversions from these regions remain untouched for ad personalization, even when transferred to linked ad accounts. Furthermore, users from a deactivated region won't be added to any lists designated for export to your linked ad accounts. However, previously exported lists remain unchanged.

### Transformations in GTM Server-Side

Transformations in a GTM server-side container serve as a powerful tool, granting you the capability to shape the event parameters emitted from your GA4 client before they're channeled to GA4 (and other) tags. This not only lets you protect sensitive data but also allows you to meticulously dictate which event parameters and HTTP headers are up for subsequent processing.

![gtm-ss-transformations](/assets/images/ga4-data-redaction/gtm-ss-transformations.png "GTM Server-Side Transformations")
_Source: [Official GTM Server-Side Documentation](https://developers.google.com/tag-platform/tag-manager/server-side/transformations)_

With transformations, you can:

- Define Precision: Share only those event parameters with tags that you've explicitly marked.
- Augment Data: Craft rules to modify existing event parameters or introduce new ones.
- Maintain Privacy: Proactively redact information by keeping certain event parameters away from tags.

The flexibility of transformations is tremendous. You can implement them across all your tags, specific tag types, or even a custom-selected group. Moreover, you can establish a series of conditions, ensuring transformations are executed only when these criteria are satisfied.

For those keen on upholding rigorous privacy standards in data collection, routing GA4 events through sGTM is a wise strategy. Furthermore, when dealing with server-to-server events, routing MP events through sGTM can ensure that the same redaction logic applies as for events collected client-side. Therefore, I strongly recommend harnessing transformations to redact PII to ensure that no personal data inadvertently finds its way to GA4.

### Data Deletion Requests in GA4

In case sensitive data slipped through your previous safeguarding measurements, GA4 offers a convenient solution: the **data-deletion request**. By leveraging this feature, you can surgically remove text data accumulated through event parameters from GA4 servers after they've been collected. Notably, even though the original text will be replaced with “(data deleted)”, the event's impact remains intact in your overall report metrics.

GA4 provides you with four options to initiate data deletion requests:

| Deletion Type                                       | Effect on Data                                                                                                                            |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Delete all parameters on all events                 | This option deletes all registered and automatically collected parameters across all collected events.                                    |
| Delete all registered parameters on selected events | This option deletes all registered parameters collected across a list of events you select in the next step.                              |
| Delete selected parameters on all events            | This option deletes registered parameters that you select in the next step across all collected events.                                   |
| Delete selected parameters on selected events       | This option deletes registered parameters that you select in the next step across a list of events that you also select in the next step. |
| Delete selected user properties                     | This option deletes user properties that you select in the next step                                                                      |

_Source: [Data-deletion requests documentation](https://support.google.com/analytics/answer/9940393?hl=en#zippy=%2Cin-this-articles)_

GA4 accommodates the removal of both automatically recorded parameters and those manually registered as custom dimensions. However, it refrains from erasing numeric parameters, text parameters based on trusted internal identifiers, and the preset entries "", "(not set)", and "(data deleted)". **Auto-collected Parameters** can be removed exclusively when you opt to erase all parameters across every event. Analytics can wipe out **custom parameters** tagged as custom dimensions. If you can't spot a specific parameter in the deletion list, it's likely it was never measured initially. Double-check the parameter's name and its registration status before deletion.

It's worth noting: if you've established a custom dimension that sources its data from an auto-collected parameter, removing the custom parameter won't affect the auto-collected one.

### GA4 User Deletion API

A somewhat related data control in GA4, but one of the lesser known ones is the [User Deletion API](https://developers.google.com/analytics/devguides/config/userdeletion/v3). Its impact on your data is more rigorous than for Data Deletion requests, as this API empowers you to facilitate the removal of all data linked to specific user identifiers. So, if any of the aforementioned methods failed and unwanted data slipped through, the User Deletion API serves you as a tool to delete data related to designated user identifiers found in your properties. Initiating these deletion requests is feasible through both Firebase projects and GA properties. To initiate a User Deletion API request, you must specify the user identifier type and the user identifier itself.

Supported user identifier types include:

- `CLIENT_ID`: Pertains to the Google Analytics Client ID.
- `USER_ID`: This is the Google Analytics User ID.
- `APP_INSTANCE_ID`: Represents the Firebase application instance ID.

It's crucial to understand that each data deletion request exclusively addresses the identifier mentioned in that particular appeal. For users linked with multiple identifiers, distinct deletion requests for every associated identifier are mandatory. If your analytics also integrates with BigQuery exports, ensure you handle deletions on that platform too.

Post the initiation of a user deletion request, the corresponding user identifier data will vanish from the User Explorer Report within a span of 72 hours. Subsequently, the data will be purged from Analytics servers during the following deletion cycle, which typically takes place roughly bi-monthly. If you've moved any of this data from Google Analytics to platforms like BigQuery, you might want to consider deleting the related identifiers there as well by running data manipulation statements.

It's worth noting that reports generated from previously consolidated data, like user counts in the audience overview report, will remain intact and unaltered - only the granular data will be removed.

## Overview of Privacy Controls in GA4

When we look at the privacy controls in GA4, we can see that they are spread across different areas of the platform and the data flow. The following diagram provides an overview of the different privacy controls in GA4 and where in the data flow they are applied:

![ga4-privacy-controls](/assets/images/ga4-data-redaction/ga4-privacy-controls.png "Overview of GA4 Privacy Controls")
_Overview of GA4 Privacy Controls - Own Visualization_

- Pre-Data Collection: This is where you prevent data from being picked up client-side altogether. Here you can utilize the **Data Redaction** feature or apply your own redaction logic using **custom variables in the GTM web container**.
- In Transit: This is where you scrub data from the GA4 requests before they hit GA4's servers. Here you can configure **Regional Data Controls** and take advantage of **sGTM's Transformations** feature.
- Post-Data Collection: This is where you delete already collected data. Here you can utilize **Data Deletion Requests** and/or the **User Deletion API**.

For a complete rundown of all available data controls in GA4, I recommend consulting [this official Google document](https://support.google.com/analytics/answer/13126616?hl=en), since it offers a central guide to GA4's data practices and controls for protecting the confidentiality and security of data collected by GA.

## Conclusion

The ever-evolving landscape of data privacy and governance has prompted platforms like Google Analytics 4 (GA4) to introduce robust measures ensuring data sanctity. GA4's suite of privacy controls, ranging from Client-Side Data Redaction to the User Deletion API, empowers GA4 users with tools that allow for fine-grained data protection. With features like Client-Side Data Redaction and transformations in GTM Server-Side, organizations can meticulously regulate the flow and processing of data, striking a balance between actionable insights and data privacy. While I like to see Google's effort in making compliance easier to manage and thereby more accessible to the broader public, I'd love to see more flexibility in the future. For instance, I miss the ability to define my own regular expressions to match my specific use cases - similar to the `customTask` feature we used to have for Universal Analytics. Unfortunately, limited customization possibilities appear to be a trend in GA4, as we're seeing it in other areas as well.

However, while these tools are incredibly powerful, they are not silver bullets. It's imperative for businesses and analysts alike to understand their intricacies and applications, ensuring they align with legal regulations and organizational standards. The obligation falls on organizations to stay updated, as platforms, regulations, and standards continuously evolve. It's equally vital to collaborate closely with legal and compliance departments, ensuring that the usage of these tools aligns with overarching data governance policies.

GA4's advancements, covered extensively in this blog post, are steps forward. They reflect a broader industry shift towards transparency, accountability, and user-centricity. By leveraging these controls effectively and responsibly, organizations can not only uphold their reputation but also foster trust among their user base, a cornerstone for long-term success in today's digital age.

**Book a meeting with me: [Calendly](https://calendly.com/gunnar-griese-gg/30min)**
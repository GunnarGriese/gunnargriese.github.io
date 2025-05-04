---
title: Server-Side Data Enrichment for GA4
author: gunnar
date: 2025-05-04 00:00:01 +0200
categories: [GA4]
tags: [ga4]
comments: true
toc: true
lang: en
---

The data in the digital analytics tool of your choice alone tells only part of your business' story. That is because actual information isn't just data points—to derive insights (=create information), you need not only data, but also context and meaning, which are just as important. For companies looking to derive actionable insights from their Google Analytics 4 (GA4) implementation (or any other analytics tool, really), this distinction is an important one.

Hence, providing additional context for your event data is vital to enriching it with meaning so that the data can eventually be transformed into insights and actions that yield business results.

Traditionally, GA4 data captures what actions a user on your website took—a page view, a button click, or a purchase. However, these events only exist in isolation without proper context, making it difficult to understand the complete customer journey. Often, business and domain knowledge transform these isolated data points into meaningful insights by connecting online behavior with additional context from other systems and real-world business outcomes.

![Additional First-Party Data Sources](/assets/img/ga4-server-side-enrichment/available-data.png)
_Additional First-Party Data Sources_

The above overview emphasizes this need, since the datasets from web & app analytics tools only make for a fraction of the overall data points collected and available to a business. The cost data from your online marketing campaigns, stock and inventory information about your products, and weather data are just as meaningful to explain your business’ performance.

For example, consider the below scenarios where critical business data lives outside your standard GA4 implementation:

1. **Disconnected systems**: Valuable customer data may be trapped in CRM systems, legacy databases, or third-party platforms that aren't directly accessible to your analytics implementation.
2. **Offline interactions**: Sales calls, in-store purchases, or kiosk interactions happen without an internet connection but still represent relevant touchpoints in the customer journey.
3. **Unsupported channels**: Certain customer touchpoints, such as connected TVs, smart home devices, and IoT products, may generate valuable customer data but are not supported by the standard tracking SDKs.

These cases are fairly common and are precisely **why** GA4 has server-side data enrichment options. When your client-side tags fall short, Data Import, Measurement Protocol, and GTM Server-Side become essential tools to fill these gaps, enable you to widen the clickstream data, and provide the context needed for meaningful analysis and data activation in connected systems, e.g., Google Ads.

In this blog post, I'll take a stab at how these server-side collection methods work, when to use each, and how they can turn your analytics implementation from simple data harvesting to a holistic measurement system that delivers true insights.

## What is server-side data enrichment?

Before jumping into the details, let's first take a step back, get the definitions right, and based on that see how these methods fit into GA4's broader infrastructure.

I (and many others) define "server-side data enrichment" as the process of gathering and/or enriching analytics data directly from a business's servers, their data warehouses, or backend  systems rather than from a user's browser or app. 

Unlike client-side tracking, where JavaScript tracking libraries or SDKs are used, server-side collection is orchestrated from within a company's own infrastructure. This allows the company to capture interactions and enrich business-relevant data points that standard client-side implementations might miss or simply cannot (or should not) access.

![Server-Side Data Enrichment Options for GA4](/assets/img/ga4-server-side-enrichment/ss-enrichment-options.png)
_Server-Side Data Enrichment Options for GA4_

Looking at the above diagram, you can see that GA4 data can be collected in many different ways before it is eventually shown to the data consumer in the interface, exposed via the API, or exported to BigQuery (BQ). We see that **traditional client-side collection from web and app clients**, captures all the event data and user identifiers directly from user devices and then sends it off to GA4's servers. Ever since the arrival of GTM Server-Side (sGTM), these client-side events can be **enriched in real-time using sGTM and Firestore** (as well as other databases/APIs), which allows adding valuable server data before sending events to GA4's collection endpoint.

A lesser-known method is server-side collection using the Measurement Protocol, where a company's internet-capable system acts as the direct source of event or user data. Additionally, Data Import functions as a separate process that provides another method to enrich client-side data with server-side information.

All these data streams ultimately converge at GA4's collection endpoint, which then distributes the information across GA4's infrastructure—powering the GA4 UI for aggregated reporting, making it available through the Data API, and exporting raw data for more granular analysis to BigQuery.

## When to use server-side data enrichment for GA4

Now, we've established the following: Server-side data enrichment methods are great at enabling  businesses to capture a more complete picture of customer interactions by bringing additional context to your analytics data. However, knowing when to implement these methods is the key to really getting the most out of these technical abilities.

Therefore, let’s have a look at the supported and most typical use cases:

* **Real-time Event Import from unsupported devices**: The Measurement Protocol allows you to track interactions from internet-connected devices that don't support standard GA4 SDKs. This includes payment systems, connected TVs (e.g., Fire TV Sticks, Applet TV, etc.), and call centers that generate customer data but lack “traditional” browsing capabilities. By implementing server-side einrichment, you can incorporate these touchpoints into your customer journey analysis in GA4.
* **Offline Conversion / Event Import**: Many significant customer interactions occur completely offline but still represent critical parts of the user journey. Data Import enables you to import conversion events that happen via phone calls, in-person interactions, or through systems that don't support standard tracking. This is particularly valuable for businesses with rather complex sales cycles where the digital showroom kicks off offline conversion activities, such as appointment bookings or consultations.
* **Offline User Data Import**: Once again, for bridging the online and offline world server-side enrichment is great as it allows you to import user attributes that are only observable in a separated environment. E.g., push data into GA4 when customer records are updated to create a comprehensive view of the customer lifecycle. Typically, we’d use Data Import (batch upload) or sGTM in combination with Firestore (realtime) to achieve this kind of enrichment.
* **Ad Cost Data Upload Import**: This one is a true classic; Understanding your marketing ROI requires connecting cost data with performance metrics. Server-side enrochment, typically through Data Import, makes it easy to import advertising impression, click, and cost data from platforms not automatically connected to GA4 (everything outside of the Google Marketing Platform). This gives you a more complete picture of marketing spend and performance across all channels, helping optimize budget allocation and campaign effectiveness.
* **Ecommerce Item Metadata Import**: Product catalogs often contain rich information that can provide valuable context for analytics. Server-side enrichment allows you to import detailed product attributes beyond what's captured in standard ecommerce tracking (and what you want to publicly disclose to your website users), including inventory status, margin information, supplier details, or other business metrics. Data Import and sGTM combined with a Firestore database can help you with widening the product data.

Now, let me mention one last, but critical piece of information: If you want to have a fully functional GA4 property and use server-side data enrichment, your setup always requires a hybrid approach. While server-side methods offer additional capabilities, **Google designed them to complement–not replace—GA4 client-side tracking**.

This hybrid necessity originates from GA4's dual nature as both an analytics platform and a marketing tool. Should you require a full-on server-side measurement approach though, I’d recommend looking into other analytics tools like Amplitude, Mixpanel, etc. that are better suited to support your needs.

## What can GTM Server-Side & Firestore do for GA4?

In previous posts, I’ve been fairly outspoken about how excited (to put it mildly) I am about the opportunities that come with integrating sGTM into a company’s measurement architecture. I am especially hyped about tapping into a company’s first-party data using sGTM and Firestore. And that is, because I’ve seen it turning sGTM into an actual data activation platform that generates money for the advertiser.

sGTM moves data processing from the user's browser to a server environment you control, e.g., on Google Cloud. Unlike the traditional client-side GTM, sGTM acts as a proxy between your website and third-party analytics platforms, giving you greater control over data collection, enrichment, and distribution.

![Use sGTM and Firestore to enrich GA4 data](/assets/img/ga4-server-side-enrichment/sgtm-enrichment.png)
_Use sGTM and Firestore to enrich GA4 data_

Firestore is a flexible NoSQL database that integrates nicely with sGTM via several variable templates to create a "first-party data ecosystem". It serves as the connective tissue between your external data sources and your analytics and marketing tagging implementation as shown in the above figure. In the context of sGTM, you can think of Firestore as another storage mechanism (like cookies and local storage) that you can read and write user or item data from, but it is you that is in full control of it.

When a user interacts with your website, sGTM can:

1. **Receive the basic event data** from the client-side data collection
2. **Query Firestore in real-time** to retrieve additional business context (user segments, predictive values, pricing, inventory, profit margins, etc.)
3. **Enrich the original event** with this server-side information
4. **Forward the now widened event data** to GA4 and other marketing platforms

This combination transforms basic user interaction data into richly contextualized business information. For example, a simple "purchase" event becomes significantly more valuable when enhanced with real-time margin data, inventory status, or customer lifetime value metrics from your Firestore database. 

The below screenshot gives you an idea of what kind of product data you could enrich, e.g., profit margins and return rates. Super relevant data points for your analysis, but probably not something you want to expose to your dataLayer for your competitors to see. With sGTM and Firestore, you can easily and securely integrate these into your measurement setup.

![Exemplary Firestore collection for documents with sensitive product data](/assets/img/ga4-server-side-enrichment/items-firestore.png)
_Exemplary Firestore collection for documents with sensitive product data_

Furthermore, you can activate the enriched data across your entire analytics & marketing ecosystem - not only GA4. Rather think about optimizing your Google Ads campaigns based on profit margins, personalizing user experiences based on offline data, or creating more sophisticated audience segments for remarketing - pretty neat and not too complicated to get started with.

Check out an earlier blog post of mine focusing on the [sGTM & Firestore integration](https://gunnargriese.com/posts/gtm-server-side-firestore-integrations/) to get more details on this topic.

## What is the Measurement Protocol?

The GA4 Measurement Protocol serves as a powerful server-side API enabling direct communication between any internet-capable system and GA4. Unlike client-side tracking methods that rely on JavaScript or SDKs, this protocol allows developers to send HTTP POST requests with event data directly to GA4's collection servers from virtually any connected device. 

As illustrated in the diagram below, this becomes particularly valuable in customer journeys that span both client-side and server-side touchpoints—notice how the first three steps (Visit Website, Research Loan Prices, Submit Loan Application) occur on a business’ website or app, while the latter three steps (Identify Applicant, Evaluate Creditworthiness, Sign Contract) happen in the real-world (e.g., customer calls, email communication, etc.), but are logged into the company’s systems.

![An exemplary user journey with offline touchpoints](/assets/img/ga4-server-side-enrichment/user-journey.png)
_An exemplary user journey with offline touchpoints_

### How the Measurement Protocol works

At its core, the Measurement Protocol functions through HTTP POST requests sent directly to GA4's collection endpoint. These requests contain structured event data and necessary identifiers to properly associate the events with the right users and sessions in your GA4 property. See an example implemented in JavaScript below:

```js
const measurement_id = 'G-XXXXXXXXX';
const api_secret = '<secret_value>';

fetch(`https://www.google-analytics.com/mp/collect?measurement_id=${measurement_id}&api_secret=${api_secret}`, {
    method: "POST",
    body: JSON.stringify({
        "client_id": "379432377.1737444724",
        "timestamp_micros": "1739540453898000",
        "non_personalized_ads": false,
        "user_properties": {
            "customer_type": {
                "value": "high-value"
            }
        },
        "events": [
            {
                "name": "purchase",
                "params": {
                    "items": [
                        {
                            "item_id": "item-id-1",
                            "item_name": "mp-blog-post",
                            "quantity": 1,
                            "item_brand": "gunnar-griese",
                            "price": 500,
                            "currency": "EUR"
                        }
                    ],
                    "currency": "EUR",
                    "transaction_id": "t-1-gg-blog",
                    "value": 500,
                    "session_id": 1743071662
                }
            }
        ]
    })
});
```

> Note: HTTP requests can be implemented using any programming language. Depending on your environment, feel free to adapt the example above. For Python, Adswerve developed a [library](https://github.com/adswerve/GA4-Measurement-Protocol-Python) that allows you to get started super easily.

As the bare minimum, each Measurement Protocol request requires the following elements:

* A GA4 Measurement ID
* A valid API secret (generated in your GA4 property: Admin > Data Streams > Select Data Stream > Measurement Protocol API secrets > Create API secret)
* A client ID or user ID to attribute the event to the correct user
* Properly formatted event parameters or user properties that follow GA4's data model

Depending on the actual use case that you’d like to achieve, two other elements play an important role, too. These are:

* `timestamp_micros`
* `session_id`  

The table below provides a crucial requirements for implementing the Measurement Protocol correctly based on your specific use case:

| **Use case** | **Session ID** | **Request time requirement** | **timestamp_micros requirement** |
|--------------|----------------|------------------------------|----------------------------------|
| **Assign User-ID to events** | Required | <= end of the session start's business day | >= session start and <= session end |
| **Correct session attribution of MP events** | Required | <= session start + 24 hours | >= session start and <= session end |
| **Export events to advertising platforms** | Not required | <= last session business day + 63 days | <= request time (not required) |
| **Send events or user properties for audience creation** | Not required | Web: <= latest online event time + 30 days<br>App: <= latest online event time + 42 days | <= request time (not required) |

As you can see, each use case has specific timing and parameter needs.

For user identification and session attribution, both require a `session_id` and specific timing constraints towards the `timestamp_micros` to maintain data integrity. The timestamp must align with the actual user session to ensure events are properly connected to the user's journey.

For advertising platform exports and [audience creation](/posts/ga4-the-cdp-you-didnt-know-you-had/), the requirements are more flexible. These use cases don't require session identification and offer extended timeframes for sending data, accommodating delayed offline conversions and backend processing.

## What is the GA4 Data Import feature?

Data Import is GA4's built-in functionality that allows you to upload external data directly into your GA4 property. Data Import is an Admin UI tool that enables non-technical marketers to upload data that cannot or is not desired to be collected by our SDKs or Measurement Protocol.

![Data Import User Interface](/assets/img/ga4-server-side-enrichment/data-import-ui.png)
_Data Import User Interface_

GA4’s Data Import functionality at the moment of writing supports a handful (it’s literally five) use cases:

1. **[Ad Cost Data Integration](https://support.google.com/analytics/answer/10071305?hl=en)**: Improve your marketing campaign performance reporting by importing advertising impressions, clicks, and costs from non-Google platforms (query time upload)
2. **[Item Data Enrichment](https://support.google.com/analytics/answer/10071144?hl=en)**: Add standard GA4 item data, e.g., Name, Brand, etc. (query & processing time join)
3. **[User Data (by client or user ID)](https://support.google.com/analytics/answer/10071143?hl=en)**: Importing CRM data or offline customer attributes (processing time upload): Enhance user segmentation and remarketing audiences by importing user metadata that you store outside of Analytics, for example, loyalty rating, date of last purchase, and CLV from your CRM system (processing time join)
4. **[Offline Event Data](https://support.google.com/analytics/answer/10325025?hl=en)**: Import events from sources that don’t have an internet connection or cannot support sending requests in real-time via the Measurement Protocol (processing time join)
5. **[Custom Event Data](https://support.google.com/analytics/answer/15086891?hl=en)**: Import data (especially custom dimensions) more flexibly to meet reporting needs/upload scenarios that are not covered by any of the above (query time join)

As you can see, it supports somewhat similar use cases as we’ve identified for the sGTM & Firestore integration and the Measurement Protocol. The unique addition that we get with Data Import is the option to also import advertising impressions, click, and costs from non-Google marketing platforms. For the other use cases though you can simply think of the Data Import as another alternative (or last resort) to get your contextual data into GA4.

### Data Import Methods: Manual vs SFTP vs Salesforce

Now, we know about the types of data we can import, but how to get the data into GA4 then? Well, currently GA4 offers two primary methods for importing data:

1. **Manual CSV Upload**: Best for occasional imports and/or smaller datasets. Simply prepare your data in CSV format, go through the mapping exercise, and upload it from your device through the GA4 interface.
2. **Automated SFTP Transfer**: Ideal for regular, scheduled imports of larger datasets. Set up an SFTP connection to automatically transfer files on a recurring basis without manual intervention.
3. (**Connect to Salesforce**: The Salesforce import option applies only to the offline-event data import type)

Yes, you see right: The Admin API option for Data Imports that you might have known from good old Universal Analytics didn’t make it to GA4. So, for now if you need frequent updates you’re left with the option of spinning up a SFTP server, since you for sure don’t want to do it manually.

> Note: For those of you being exposed to the term “SFTP” for the first time: An SFTP (**S**ecure **F**ile **T**ransfer **P**rotocol) server is a secure file storage system that enables encrypted file transfers over a network. Eventually, it functions as a digital drop box where files can be deposited and retrieved by GA4 using the SSH File Transfer Protocol.

For the future, I am hoping to see a BQ import option emerge - similar to the [Data Manager](https://support.google.com/google-ads-data-manager/answer/13761872) that Google offers for Google Ads. Given the general trend of digital analytics/marketing and the cloud converging more and more, it would just make sense to see this come to life sooner rather than later. So, let's cross our fingers for this!

### How do the joins work?

Once you’ve created your desired data source (a CSV file or a SFTP server) and then mapped the GA4 dimensions (or "fields") to the respective columns in your data source’s CSV (s. below screenshot), you’ve completed the data import into GA4.

![Data Import Mapping (item data)](/assets/img/ga4-server-side-enrichment/data-import-mapping.png)
_Data Import Mapping (item data)_

Now, a data source has been configured defining where the imported data is coming from and where you'll find it in your GA4 property. That also means you can simply update the underlying data (like updating the data source with a CSV file with nice and fresh data) as long as the schema of the file remains intact. Only if you need to adjust the mapping (e.g., add or remove a column), you'll need to create a new data source from scratch.

Let's double click on how the "external" data is joined with your GA4 data collected from the users' devices. GA4 offers two distinct approaches to joining imported data with your analytics data.

#### Collection/Processing Time Joins

Processing time joins **happen as GA4 receives and processes incoming events**.

Data is matched and combined during the data collection phase at the collection endpoint. Once processed, the join becomes permanent, affecting all downstream reports and exports, and cannot be reverted - data deletion requests are the only way to remove this data again. These joins are commonly used for item data enrichment and user property imports. While more rigid in nature, they provide consistency across your entire GA4 property and result in the data also being exported to BigQuery.

For example, when you import CRM data using User Data enrichment, GA4 will permanently associate those attributes with users in your events as they're processed.

#### Reporting/Query Time Joins
Query time joins occur dynamically when a report is generated.

Data is matched on-demand and only when you make a report request, e.g., within the GA4 UI. These joins only affect specific reporting views without modifying the underlying data. They are primarily used for ad cost data imports, though item data import uses both query and collection time joins. Reporting/Query Time Joins result in greater flexibility as the imported data remains separate from the original event data, which allows the imported data to be applied retroactively to past data and makes its removal as easy.

So, processing time joins bind the client- and server-side data together as if they would have come from the same source and would have been collected together. The query time joins are happening “on the fly” in the background, when you are building a report in your GA4 interface.

### The Critical Element: Joining Keys

As with every data join operation, the success of the GA4 data imports depends on correctly matching keys between your GA4 data and imported data. If you ever attempt to use the Data Import feature, I recommend checking out [Google’s official documentation](https://support.google.com/analytics/answer/10071301?hl=en) where they share CSV templates for each of the import types. For your quick reference, you can find the currently required join keys below:  

* For user data: User ID or client ID
* For item data: Item ID
* For event data: Client ID, measurement ID, event name
* For cost data: Campaign source (required), campaign medium (required), date (required), campaign name (optional), campaign ID (optional, previously required)

The remaining columns of your CSV file will be imported to their mapped dimensions or metrics as specified in the previously mentioned mapping. Once imported, they are available for your use in GA4.

![Data Import Match Rate](/assets/img/ga4-server-side-enrichment/data-import-match-rate.png)
_Data Import Match Rate_

To give you a feeling for how well your import efforts are going, GA4 gives you quality stats telling you the share of provided rows that have actually been imported (% Imported) as well as the ratio of keys in the imported CSV file that can be found in your property within the last 90 days (match rate).

## Side-by-Side Comparison

The table below provides a quick reference guide for comparing the three server-side data enrichment methods available for GA4. Each approach offers distinct advantages and trade-offs across implementation complexity, real-time capabilities, historical data handling, flexibility, maintenance requirements, and team suitability.

|  | **sGTM + Firestore** | **Measurement Protocol** | **Data Import** |
|--|---------------------|-------------------------|----------------|
| **Implementation complexity** | **Low to Moderate** - sGTM setup is simple, Firestore setup might require data engineering support | **Moderate,** requires developer support | **Low (CSV uploads),** moderate when using SFTP import |
| **Real-time Capability** | **Yes** - real-time enrichment at collection time | **Yes** - real-time event sending | **No** - batch processing with scheduled imports (for events). Metadata enrichment is "real-time". |
| **Backfill capability** | **No** - historical data cannot be enriched | **Yes (with limitations)** - using timestamp_micros event scan be send to the "past" | **Yes (with limitations)** - import types that support query time joins allow for enrichment of historical data |
| **Flexibility** | **High** - sGTM allows transformation/enrichment for entire request | **High** - structured API but customizable payloads | **Limited** - predefined schemas and formats |
| **Maintenance Requirements** | **Higher** - requires monitoring of server-side components and Firestore data source | **Medium** - API changes must be tracked | **Lower** - mostly UI-driven maintenance |
| **Suitable for:** | Teams with some technical support<br>Advanced implementations<br>Complex data orchestration needs | Teams with development/engineering<br>Automated server integrations<br>Custom applications | Marketing teams (last resort)<br>Analysts with minimal technical resources<br>Scheduled/periodic data uploads |

While sGTM with Firestore excels in real-time processing and flexibility (ideal for teams with technical resources), the Measurement Protocol offers developer-friendly direct integration for custom applications. Data Import provides the most accessible option for marketing teams with limited technical support but sacrifices some flexibility and real-time capabilities.

Consider your organization's technical resources, use cases, and data requirements when selecting the appropriate method for your implementation. The right choice depends on balancing these factors against your specific business needs and analytics goals.

## Summary

Server-side data enrichment is no longer a luxury but a necessity for businesses seeking comprehensive analytics insights. This blog post has explored three powerful approaches GA4 offers: Data Import for batch uploads, GTM Server-Side with Firestore for real-time enrichment, and the Measurement Protocol for direct server-to-server communication.

Each method serves distinct use cases and fills specific gaps in your measurement strategy. While client-side tracking remains fundamental, these server-side approaches allow you to incorporate critical business context from offline touchpoints, backend systems, and proprietary data sources that traditional tracking methods simply cannot access.

Remember that the most effective GA4 implementations use a hybrid approach, strategically combining client and server-side methods to create a comprehensive view of your customer journey. When implemented correctly, these enrichment techniques transform GA4 from a simple analytics tool into a robust business intelligence platform that delivers actionable insights based on the complete picture of your customer interactions.

Having trouble implementing these techniques in your own GA4 property? Need guidance on which approach best fits your specific business requirements? Feel free to reach out — I'm here to help navigate the complexities of server-side data enrichment and ensure your GA4 implementation delivers maximum value for your organization.


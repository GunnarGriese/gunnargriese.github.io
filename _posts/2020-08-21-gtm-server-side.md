---
title: GTM Server-Side Tagging – Better Data & More Control
author: gunnar
date: 2020-08-21 15:24:15 +0200
categories: [GTM]
tags: [ga4, gtm-server-side]
comments: false
---

Over the last many months we have been running a series of beta tests and projects for a group of selected clients to get both practical experience and to help optimize the recently released Google Tag Manager (GTM) server-side tagging setup.

Our ambition is to provide both background information and context to why we think most businesses should seriously consider adopting it to better support the business. Moreover, you will get an overview of the feature’s functionality and possible use cases to move towards a future-proven, first-party tracking setup, improve overall customer experience, and gain full control over your data.

The main takeaway is that GTM server-side will increase flexibility and control over your data and enhance the durability and the direct business value of the solution far beyond what is possible with a traditional Google Tag Manager setup.

## Privacy First and 1st Party Analytics

Nowadays businesses face many challenges that require them to rethink the way they do website and app tracking. Luckily, these challenges with GTM server-side will also open up many agile opportunities for companies willing to adapt and change. However, traditional tracking is being confronted by a lot of challenges that will make “tracking as usual” technically impossible.

One of these challenges is the new “Privacy first”-paradigm imposed upon us by regulations like GDPR (EU) and CCPA (California). Browser providers have also become much more privacy-aware within the last couple of years, seeking to better protect their users’ data from all too data greedy adtech tools.

Similarly, initiatives like Safari’s “Intelligent Tracking Prevention” (ITP) and Firefox’s “Enhanced Tracking Prevention” (ETP) heavily restrict access to frequently used browser storage options (esp. cookies and local storage). Google also just recently announced that they will phase out third-party cookies altogether within the next two years for their Chrome browser (a so-called “privacy sandbox” will replace third-party cookies).

Too often advertisers have also implemented Javascript snippets on their websites without being aware of its full functionality, resulting in handing over control over their users’ data to unknown third-parties and making massive data breaches possible in the first place.

Therefore, we should welcome the general direction of these actions taken since it helps to secure our personal data, to mature the industry, and to regain long-lost credibility – aiming to end questionable “wild wild west”-tracking practices.

The main downside to this movement is that it also affects and creates biases in business-critical data collection based on user consent: The technical and regulatory environment that traditional website and app tracking are embedded in makes it difficult for us to keep track of specific user behavior – increasing our blindspot in understanding a user’s needs.

## GTM Server-Side Tagging to the Rescue

Google Tag Manager (GTM) now comes with a new feature (in beta status for the moment) that will enable businesses to create a 1st-party analytics setup. GTM server-side tagging has arrived to change how website and app tracking are implemented, and how data is shared with third-parties. Follow along to understand how this feature will help you improve website user experience, increase security of your users’ data, and increase control over your data collection.

### How does it work?

While the GTM server-side container provides new tools and features to measure user activity, the general model of tags, triggers, and variables remains untouched.

![gtm-server-side-architecture](/assets/img/gtm-server-side/server-side-tagging.png)
_Source: https://developers.google.com/tag-platform/tag-manager/server-side/intro_

GTM Server-side tagging translates to a new “Server” container running on an App Engine instance – (ideally) mapped to your domain namespace – in your own Google Cloud Platform (GCP) project. It is then possible to send HTTP requests to the server from the user’s device or any other device with an internet connection. The GTM server turns those requests into events that are processed by the container’s tags, triggers, and variables.

While the well-known concept of tags, triggers, and variables work as they used to on client-side GTM containers, the newly introduced “clients” is the glue between the devices sending requests and the container logic. The client can receive and claim requests (and data sent with it), parses them into one or more events, routes data to be processed in the container (tags, triggers, and variables), and returns an HTTP response to the requesting device.

### Gain Data Control and Flexibility

What is different about this approach than tracking based on client-side Javascript and pixels, is that you have full control and gain flexibility over how the data is processed until you send it to third-party tools (enabling hit validation, PII controls, etc.). In fact, since the GTM server (https://gtm.example.com) is associated with the same domain as your website (https://example.com), every interaction between them is considered to be a first-party data exchange by the user’s browser.

### Mitigate the Impact of Browser Tracking Prevention and Ad Blockers

By this change of context, significant restrictions forced upon us by browser tracking prevention will be circumvented, because you gain the ability to set first-party HTTP cookies (e.g., GTM server-side introduces a new FPID cookie). For example, now Safari’s ITP will no longer restrict the lifetime of cookies associated with Google Analytics when placed from the server-side resulting in better data quality for reporting and analysis (especially relevant for businesses with a young and tech-savvy user base). Keep in mind that this power comes with great responsibility, and you should always be aware of the legal and ethical implications of setting cookies and the data you collect.

## What Use Cases Can Be Revealed?

GTM Server-side tracking restores transparency in third-party tool and website usage, but beyond that, there are a few other advantages when you track events on the server-side that can lead to strong use cases for the business.

### Improved Data Accuracy and Control

Data accuracy can be improved even more when businesses decide to leverage server-to-server communication for business-critical events like transactions. We have all experienced discrepancies between the number of transactions in Google Analytics (GA) and CRM systems due to ad blockers and other side-effects when relying on client-side tracking (page reloads, etc.). This can be mitigated by removing client-side tracking of transactions and sending the required data points directly from your CRM systems to the GTM server, passing it on to GA for analysis.

### Improved Page Load Speed and Data Security

In general, server-side tracking can remove the processing burden from a given browser and move it to the cloud. Since one HTTP request is enough to trigger an event in the server-side container, it can trigger multiple tags in the server-side environment. For example, the client could send one HTTP request on every page load, triggering a pageview hit for GA and Facebook at the same time. Given that no Javascript written by Facebook would need to be executed in the user’s browser, with server-side tracking it may be possible to increase page load speed. Since this will positively affect overall user experience, this has the potential to increase your conversion rates.

### Smooth Integration to the Google Cloud Platform

Furthermore, because the GTM container is executed in Google’s cloud integrations, other GCP resources like BigQuery, ML Engine, and Cloud Functions will most likely be integrated soon. This will open up a lot of possibilities for advanced use cases involving machine learning and (event-based analytics)[https://gunnargriese.com/posts/ga4-the-cdp-you-didnt-know-you-had/].

Once this new GTM feature moves out of the beta phase after being improved based on feature requests and active community members’ contributions, even more possibilities will be available, significantly changing tracking implementations based on GTM.

## Closing Thoughts

The GTM server-side container’s release continues a general trend that can be observed for many Google Marketing Platform tools: Strengthen tool integration and push towards GCP. By pursuing this strategy, Google ensures a smooth data flow between systems and, at the same time, increases each tool’s functionality to cope with the ever-changing adtech environment.

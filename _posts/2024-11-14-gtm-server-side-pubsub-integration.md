---
title: GTM Server-Side Pantheon - Part 2 - Integrate Pub/Sub into GTM Server-Side
author: gunnar
date: 2024-09-14 00:00:01 +0200
categories: [GTM]
tags: [gtm-server-side]
comments: true
---

## What is Pub/Sub?
At its core, Pub/Sub (short for Publish/Subscribe) is a messaging service provided by Google Cloud that facilitates the asynchronous exchange of messages between different systems. It’s designed to be highly scalable, reliable, and low-latency, enabling real-time communication between applications across various environments.

Think of it as a distributed event-driven system where different components of an architecture can communicate without directly depending on one another. This decoupling of services makes it a powerful tool for event-driven systems, but in the context of GTM Server-Side (sGTM), its capabilities can unlock a whole new layer of real-time data processing and orchestration.

![Pub/Sub High Level Flow](/assets/img/gtm-ss-pubsub/pubsub-high-level-flow.png)

Here’s how Pub/Sub works:

* **Publishers** are entities that send messages (events or data) to a **topic**. These messages can be anything from user events to system logs. In the context of this blog post, sGTM acts as a publisher, sending events to a Pub/Sub topic.
* **Topics** are channels through which messages are exchanged. They act as a mailbox where publishers can drop messages, and subscribers can pick them up.
* **Subscriptions** are the connections between topics and subscribers. They define the rules for how messages are delivered and processed. 
* **Subscribers** are entities that are interested in receiving messages from a topic. They listen to the topic and can act on incoming data as needed, triggering various processes. This can be anything from storing data in a database to triggering a Cloud Function - your imagination is the only limitation here.

For example, an e-commerce website might use Pub/Sub to trigger different actions: a "purchase" event could be published by one part of the system and consumed by several subscribers, such as inventory management, email marketing, and analytics systems, without needing these components to directly interact with each other.

**But I wonder if they will be as reliable as Pub/Sub, which guarantees at least once delivery.**

In the context of GTM Server-Side, Pub/Sub can be used to collect and forward important events like user interactions or backend events. This makes it easy to integrate event-driven architectures, allowing you to expand your GTM setup beyond traditional tracking and into real-time, cross-system orchestration. Whether you need to trigger downstream processes, send events to a third-party system, or store them in a database for further analysis, Pub/Sub’s flexibility allows for these seamless integrations.

## Why send clickstream data (e.g., GA4) to Pub/Sub?

Once you have your data flowing through Pub/Sub, you can route it directly to a whole slew of GCP services, such as Cloud Functions, Cloud Run, DataFlow, BigQuery, Cloud Build and others. These services can do more above and beyond what a JavaScript tag or client can do, so subsequently you can expand the horizons on what your digital analytics data can do.

This can include triggering workflows for:

sending emails or triggers to yourself (A customer just bought this!)
sending something to the customer themselves if you know them (You just bought this!)
Transforming and filtering your GA4 data, perhaps by using the Data Loss Prevention API to redact credit card numbers, email address etc before it hits BigQuery
Enriching GA4 data with other data (such as 1st or 2nd party data)

## Hermes - The Messenger of the Gods

Hermes is the messenger of the gods in Greek mythology. How fitting that Google decided to name their Pub/Sub GTM Server-Side custom template after him. The [Hermes solution](https://github.com/google-marketing-solutions/gps-sgtm-pantheon/blob/main/sgtm/hermes/README.md) is a sGTM custom **tag template** that allows you to send event data to Pub/Sub. 

![Hermes Tag Template](/assets/img/gtm-ss-pubsub/hermes-tag-template.png)

`getGoogleAuth` authenticates the sGTM instance with Pub/Sub. It uses the service account running the container to get the necessary credentials for making authenticated requests to GCP services. So, make sure to grant this service account `roles/pubsub.publisher` rights.
Does some type conversion based on the key (key with suffix `_int` is converted to integer, key with `_num` is converted to number, otherwise it's a string).
`toBase64` payload is encoded to base64. Make sure to decode it in the subscriber.
`sendHttpRequest` sends the payload to Pub/Sub.

## Using GTM Server-Side and Pub/Sub to power a real-time dashboard

The idea is to build a realtime dashboard that allows to monitor detailed information about the incoming events. This could be useful for debugging, monitoring, or just to get a better understanding of the data flowing through your system.

![Real-Time Dashboard](/assets/img/gtm-ss-pubsub/pubsub-realtime-dashboard.png)

Hermes tag writes item data to Pub/Sub `items-realtime` topic, the subscription pushes new messages to a Cloud Run service that processes the data and stores it in Firestore (in our case, we simply increase the `counter` attribute).

```json
[ 
    { "item_id": "123", "item_name": "Blazer", "price": 150, "quantity": 1, "currency": "DKK" }, 
    { "item_id": "456", "item_name": "T-Shirt", "price": 30, "quantity": 2, "currency": "DKK" } 
]
```

The outcome is a Firestore collection that holds a document for each item. Each item has a `counter` attribute that is increased by the quantity of the item in the event and additional product information (e.g., price, item_category, profit, etc):
![Firestore Document](/assets/img/gtm-ss-pubsub/firestore-document.png)

> Add video here
> ADD PROFIT TO THE DASHBOARD

Find the code for the processing service and the dashboard in this [GitHub repository](https://github.com/GunnarGriese/firestore-realtime-dashboard).

### Conclusion

By integrating Pub/Sub with GTM Server-Side, you can unlock new use cases and expand the capabilities of your data collection and processing. Whether you need to trigger downstream processes, send events to third-party systems, or store data for further analysis, Pub/Sub provides the flexibility and scalability to meet your needs.
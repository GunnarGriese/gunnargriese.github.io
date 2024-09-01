---
title: Unleash the Potential of PostHog Analytics Platform with Google Tag Manager
author: gunnar
date: 2023-04-10 08:24:15 +0200
categories: [GTM]
tags: [gtm, custom-templates, posthog]
comments: false
---

In today’s data-driven world, understanding user behavior is crucial for any business. Product analytics platforms like PostHog have emerged as essential tools for gaining insights into how users interact with your website or app. In this blog post, we will explore the PostHog analytics platform, its SDKs, the JavaScript SDK in particular, Google Tag Manager tag templates, and how you can integrate PostHog with Google Tag Manager using a custom tag template.

## Introduction to PostHog Analytics Platform

[PostHog](https://posthog.com/) is an open-source product analytics platform that helps you analyze user behavior on your website or app. It provides event-based tracking, funnel analysis, user segmentation, and other essential features to help understand how users engage with the product you are responsible for. It sits in the same space as tools like Mixpanel, Heap, and Amplitude which are all specializing in providing product managers and analysts with the required insights to optimize their platform towards their users’ needs.

If you are looking for a deep-dive on how Product Analytics differs from Marketing Analytics, I recommend checking out [Adam Greco’s blog series](https://amplitude.com/blog/marketing-analytics-vs-product-analytics-part-1) on that topic.

## PostHog SDKs for Data Collection

PostHog itself offers a variety of SDKs (Software Development Kits) to make it easy for you to collect data from different platforms:

- JavaScript: For tracking user interactions on websites.
- Python: For backend applications or data pipelines.
- Ruby: For Ruby on Rails applications.
- PHP: For PHP-based applications.
- Go: For applications written in Go.
- Node.js: For server-side JavaScript applications.
- Android: For Android apps.
- iOS: For iOS apps.

These SDKs enable you to implement PostHog tracking in your application or website, regardless of the technology stack you’re using.

## Details on the JavaScript SDK

The [PostHog JavaScript SDK](https://posthog.com/docs/libraries/js) is the most widely used SDK for tracking user interactions on websites. It provides a simple API to send events, identify users, and manage user properties. You can track custom events, page views, clicks, form submissions, and more with minimal code.

The SDK also supports advanced features like autocapture, which automatically tracks user interactions with your website without requiring additional code. You can configure the SDK to suit your needs, such as disabling certain features or customizing how data is captured.

## Google Tag Manager Custom Templates

As I personally spend most of my time working with Google Tag Manager (GTM) and Google Analytics (GA), GTM is actually my preferred tool when it comes to implementing JS tracking code on websites or web apps and is widely used. If your organization is not only engaging in product analytics, but also actively running digital marketing campaigns, there is a high chance that your product has GTM embedded already.

Google Tag Manager (GTM) is a powerful tool that allows you to manage and deploy marketing tags, analytics tracking, and other code snippets on your website without the need for manual code updates. GTM uses tag templates, which are pre-built code snippets that can be customized to suit your specific tracking requirements.

Tag templates help streamline the process of implementing third-party tracking scripts, like PostHog, on your website. They allow you to configure tracking settings without editing code directly, making it easier to manage and maintain your tracking implementations. These templates can be submitted to the GTM Template Gallery and are then available to everyone who would like to use them.

The catch is that PostHog has not yet published an official template to run their JS SDK through GTM. That is why I set out to bring (most of) the functionalities of PostHog’s JS SDK to GTM without the need to deploy any [(potentially harmful)](https://web.dev/tag-best-practices/#be-careful-with-custom-html-tags:~:text=Be%20careful%20with%20Custom%20HTML%20tags%20%23) custom HTML tags.

## Integrating PostHog with Google Tag Manager Using the Provided Template

The provided PostHog GTM tag template makes it simple to integrate PostHog tracking into your GTM container.

![posthog-event-template](/assets/img/posthog/posthog-custom-event.png)
_Custom Event with event parameters implementation using the GTM template_

With this template, you can manage events, user properties, and configuration settings directly from your GTM workspace. Here’s what you can do with the template:

- Initialize PostHog with various configuration options.
- Capture events and virtual pageviews with custom properties.
- Identify users with user properties.

See below for some examples of the GTM template functionalities.

### Initialization — Basic Configuration

![posthog-config-tag](/assets/img/posthog/posthog-config.png)
_Exemplary configuration of the Initialization tag_

See detailed documentation for each of the configuration options here. The configuration options represented in the tag template are:

- apiHost: The domain of your PostHog instance (e.g., `https://app.posthog.com`). The tag will append `/static/array.js` to this value to build the actual request URL.

- `apiKey`: Your PostHog project API key
- `autocapture_tuning`: Custom allowlist settings for autocapture.
- `autocapture_off`: Disable autocapture completely .
- `capture_pageview`: Enable/disable capturing pageviews.
- `capture_pageleave`: Enable/disable capturing page leave events.
- `cross_subdomain_cookie`: Enable/disable cross-subdomain cookie tracking.
- `disable_persistence`: Enable/disable cookie/localStorage persistence.
- `disable_session_recording`: Enable/disable session recording.
- `enable_recording_console_log`: Enable/disable console log recording.
- `mask_all_text`: Enable/disable masking all text.

### Initialization — Advanced Tracker Configuration

![posthog-callback](/assets/img/posthog/posthog-callback.png)
_Exemplary callback function_

The PostHog library can be initiated with a _callback_ (e.g., call `identify`) that is executed once the library has loaded.

For the callback function to work in the GTM template version, you need to reference a custom JS variable in the field `loaded` (s. screenshot in section Basic Configuration) that returns a function.

As soon as the PostHog scripts are handled and the tracker is initiated, this function will be executed.

### Custom Events, User Properties, and Event Parameters

![posthog-event-params](/assets/img/posthog/posthog-event-params.png)
_Exemplary custom event tag implementation_

Using the GTM template, you can effortlessly track custom events (as well as well virtual pageviews) and augment them with fine-grained event parameters, providing a comprehensive understanding of user engagement patterns. Furthermore, the template adopted the JavaScript SDK functionality which allow you to set user properties using both `$set` and `$set_once` methods, giving you the flexibility to choose between updating values or preserving the initial user attributes.

## How to get started?

Please feel free to [download the template](https://github.com/GunnarGriese/gtm-template-posthog) from my GitHub and give it a spin. I am happy for any feedback to improve the template, include more functionalities from the original SDK, and fix potential bugs as they arise.

To use the template, simply import it into your GTM workspace, create a new tag using the template, and configure the settings based on your needs. This integration ensures that you can take full advantage of both PostHog and Google Tag Manager to gain insights into user behavior on your website or app.

While this article outlines an approach on how to implement PostHog through GTM, you might want to refer to PostHog’s great and easy-to-follow [documentation](https://posthog.com/docs/getting-started/start-here) on how to get started with their platform.

## Summary

In conclusion, PostHog is a powerful analytics platform that can help you understand your users better. By integrating it with Google Tag Manager using the provided tag template, you can streamline the implementation process and efficiently manage your tracking setup. This combination of PostHog and Google Tag Manager will hopefully help speeding up implementation projects and empower you to make data-driven decisions even faster. So go ahead, explore the potential of PostHog analytics platform and Google Tag Manager integration, and unlock new insights into your users’ behavior.

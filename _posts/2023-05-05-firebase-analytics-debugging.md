---
title: Debugging Google Analytics Tracking for Mobile Apps - A Guide for Beginners
author: gunnar
date: 2023-05-05 11:24:15 +0200
categories: [GA4, Firebase]
tags: [ga4, firebase analytics, charles proxy, gtm, ios debugger]
comments: false
---

# Debugging Google Analytics Tracking for Mobile Apps: A Guide for Beginners

## 0. Introduction

Are you a digital analyst looking to implement and debug Google Analytics tracking via Firebase for your mobile iOS apps and have no clue where to start? This blog post is for you! I’ll briefly walk you through the process of setting up Google Analytics tracking using both the Firebase SDK and Google Tag Manager (GTM). Primarily, I’ll cover the most effective debugging tools, including Charles Proxy and David Vallejo's iOS/Android Debugger, to help you achieve accurate and reliable data collection.

## 1. Introduction to Google Analytics Tracking for Apps

Google Analytics 4 (GA4) marks the debut of a unified platform for tracking both web and mobile app data in Google’s analytics suite. This change acknowledges the increasing trend of businesses viewing their websites and mobile apps as interconnected, rather than separate sales channels. GA4 is designed to provide a more comprehensive understanding of user interactions across various platforms.

As GA4 integrates web and app analytics more closely, digital analysts must expand their knowledge of app tracking to fully leverage GA4’s potential. Traditionally, most digital analysts focused primarily on website measurement implemented via Google Tag Manager (GTM) or gtag.js.

![ga4-data-collection](/assets/img/firebase-debug/ga4-data-collection.png)
_Source: https://developers.google.com/analytics/devguides/collection/protocol/ga4_

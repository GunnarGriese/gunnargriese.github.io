---
title: Consent Mode v2 - A Comprehensive Technical Guide
author: gunnar
date: 2024-01-31 00:00:01 +0200
categories: [GA4]
tags: [ga4, gtm, gtm-server-side, consent-mode, firebase-analytics]
comments: true
---

In fall 2023, the EU has deemed [Google as a gatekeeper](https://blog.google/outreach-initiatives/public-policy/building-for-compliance-with-the-digital-markets-act/) in the digital space under the Digital Markets Act (DMA), placing it under heightened legal scrutiny. In response to this assessment and to meet the DMA enforcement deadline in March 2024, Google is adjusting its advertising solutions. One aspect of this change is the latest update to Google Consent Mode. Starting in March 2024, Consent Mode will become mandatory for all advertisers operating in the EEA and wanting to use all of Google’s GMP advertising features. This shift, which includes [phasing out certain features in the remaining UA360 properties](https://support.google.com/analytics/answer/11583528?hl=en#:~:text=before%20this%20date.-,For%20Google%20Analytics%20360%20customers,-Universal%20Analytics%20360) while at the same time providing insufficient documentation on the new feature's functionality and behavior, left the community with a lot of open questions.

This blog post is the product of me penning down my observations and combining them with the ones from my peers in the industry to contribute to a better understanding of Google's Consent Mode v2 and its impact on data collection. Overall, the aim is to provide readers (and me as the author) with a comprehensive overview of Consent Mode v2 and help them make informed decisions about their website's privacy and data practices by unveiling the technical intricacies.

This blog post can be seen as the technical counterpart of [my previous thoughts on Consent Mode v2](https://iihnordic.com/news/update-of-consent-state-and-its-impact-on-advertisers/?ref=gunnargriese.com) published on the IIH Nordic blog. If you are new to the topic, I recommend reading the previous blog post first to get a better understanding of the topic's context and the implications of Consent Mode v2.

Read the full article on [IIH Nordic's website](https://iihnordic.com/).

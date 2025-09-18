---
title: Moving Beyond Basic Conversion Tracking - Engineering Signals for Sustainable Marketing Advantage
author: gunnar
date: 2025-09-17 00:00:01 +0200
categories: [GTM, GA4]
tags: [gtm-server-side, ga4]
comments: true
toc: true
lang: en
---

"What signals are you actually using to optimize your marketing campaigns?" This is the question I've started asking clients after witnessing many businesses struggle with rising ad costs while their optimization levers continue to disappear.

Nine out of ten times, the answers default to the expected standard: They send basic conversion events (1 lead) or simple revenue values (€100 order) to platforms like Google Ads and Meta, while at the same time wondering why their ROAS keeps declining and budgets get tightened as a result.

However, it doesn't have to be like that: There are far more efficient ways to optimize a marketing budget and ensure a high ROI. From a technical perspective, these solutions have never been easier to implement, yet few are aware of them. 

In this first article of my series, I'll outline the shift needed in how we think about marketing signals. You can think of it as the overarching concept behind what I've previously explored in my [GTM Server-Side use cases post](https://gunnargriese.com/posts/gtm-server-side-use-cases/). The following posts in this series will focus more on the" how?" of building these systems. So, let's get started!

## The Optimization Playbook Has Changed

The trend for marketing campaign optimization is clear. Your campaign management is becoming increasingly automated, and larger shares of marketing budgets are being optimized with "intelligent" in-platform tools, such as Performance Max (GMP) and Advantage+ (Meta). 

![Inner workings of ad platforms](/assets/img/signal-engineering/signal-engineering.png)
_Inner workings of ad platforms_

Various, complex aspects of the process such as attribution modeling, bidding strategies, and incrementality measurement are already handled by the platforms themselves today. Hence, the influence you as the advertiser have over campaign performance is limited mostly to two aspects:

1. Creative content (ad copy, visuals, etc.), which AI tools will likely automate further as well
2. Outcome signals designed and sent back to the platforms by the advertiser

These signals are critical because they directly train the machine learning algorithms on what constitutes a valuable outcome for your business. The platforms use these signals to identify patterns in user behavior, refine targeting models, and adjust bidding strategies in real-time. Essentially, your signals instruct the algorithm on what constitutes "success," which in turn determines how it optimizes future ad delivery and audience targeting.

Think of it this way: instead of telling Meta "this person bought something for €200," you could say to it "this person has an 85% probability of becoming a high-lifetime-value customer based on our proprietary scoring model." Which signal do you think will help the algorithm find more valuable prospects for your specific business?

While businesses invest in creative design and testing, only a few are focusing on the signals they report back to the platforms. But the most advanced ones have already started building systems that create proprietary signals to train ad platform algorithms toward their specific business outcomes.

## Value-Based Bidding: Optimizing Toward Real Business Outcomes

As I’ve laid out in one of my [previous blog posts](https://gunnargriese.com/posts/gtm-server-side-use-cases/), there’s a reason why your business defaults to the standard practice, though: The last time you tried to shift away from this logic, you likely faced an impossible trilemma. You can either send sensitive profit data through browsers and risk security exposure, use generic revenue values that lead to suboptimal targeting, or upload data in batches, missing real-time optimization opportunities.

This trilemma forced you and other companies down a predictable path: The suboptimal one! But what could more promising alternatives actually look like?

![Exemplary Signals](/assets/img/signal-engineering/signals-examples.png)
_Exemplary Signals_

Real-time profit optimization represents the first evolution beyond generic revenue tracking. When someone makes a purchase, rather than sending the transaction amount, your system calculates the actual contribution to your bottom line. This includes factoring in product costs, shipping expenses, operational overhead, and return probabilities. The advertising platform then optimizes toward customers who generate actual profit rather than just revenue volume.

Even more powerful is predictive lifetime value signaling. Machine learning models trained on historical customer data can predict which new customers are likely to develop into long-term, valuable relationships. Instead of optimizing for high first-purchase values, your campaigns target prospects who share characteristics with your most profitable existing customers. This fundamental shift moves optimization from transactional thinking toward relationship value.

The most advanced implementations involve dynamic value adjustments based on current business conditions and the business context. Inventory levels, seasonal demand patterns, customer acquisition costs by segment, and churn probability all factor into real-time value calculations. A winter coat sale in December might warrant higher bidding than the same product in March, not because the revenue differs, but because the strategic business value changes.

## Conclusion

The question you need to answer is: **Are you building the infrastructure that will give you a sustainable competitive advantage, or are you content to compete on the same level as everyone else with generic signals and hope your creatives are better?**

Your window to establish this advantage is narrowing. Platform automation is accelerating, ad costs continue rising, and the businesses that move first on designing proprietary outcome signals will create a competitive advantage that becomes increasingly difficult for competitors to cross. The irony is that while the technical implementation has never been more accessible, the strategic advantage of early adoption has never been more pronounced.

This article explained the strategic "why" behind advanced marketing signals. In the next article, I'll have a closer look at the tactical "how" – walking through the specific technical implementations, tools, and architectures needed to build these proprietary signaling systems. The path forward starts with acknowledging that in today's advertising landscape, the quality of your outcome signals determines the quality of your customers, and the infrastructure to engineer signals your competitors cannot match has never been more within reach.

As always, if you have any questions or want to discuss this topic further, feel free to reach out to me directly or leave a comment below.

> Shout out to [Rick Dronkers](https://www.linkedin.com/in/rickdronkers) and [Eric Seufert](https://www.linkedin.com/in/ericseufert) for bringing the term "Signal Engineering" in the marketing context to my awareness - a concept that I've been tinkering with, but simply lacked the vocabulary to articulate. Make sure to follow them for more insights on this topic.
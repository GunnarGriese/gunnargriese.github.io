---
layout: post
title: Analytics in the Age of AI - Why Fundamentals Still Matter
description: A write-up of the first Analytics DevNet Webcast with Simo Ahava, Steen Rasmussen and Jomar Reyes. AI makes analytics faster, but speed alone doesn't create expertise - data quality, mental models and organisational integration still decide whether measurement is trustworthy.
author: gunnar
date: 2026-09-01 00:00:01 +0200
categories: [GA]
tags: [ga, ai, webcast]
image: /assets/images/blog/analyticsdev-webcast.jpg
comments: true
toc: true
lang: en
---

When an LLM can write your GTM custom template, your BigQuery SQL and the explanation of what both do in about eleven seconds, what exactly is left of "analytics expertise"? That's the question Steen Rasmussen, Jomar Reyes and I put to Simo Ahava in the very first episode of the Analytics DevNet Webcast. The short answer we landed on: AI makes analytics faster, but speed alone doesn't create expertise. The practitioners who stay valuable are the ones who can tell when a confident-looking answer is quietly wrong (and can explain as to why that is the case).

{% include newsletter-cta.html %}

## Watch the episode

<div style="width:100%; height:0; position: relative; padding-bottom:56.25%"><iframe title="Video Player" src="//blc.twentythree.com/v.ihtml/player.html?source=embed&photo%5fid=130975359" style="width:100%; height:100%; position: absolute; top: 0; left: 0;" frameborder="0" border="0" scrolling="no" allowfullscreen allow="autoplay; fullscreen"><p>Your web browser does not support iframes, which means that the video cannot play.</p></iframe></div>

If you'd rather read than watch, the rest of this post is my write-up of the conversation with the caveat that I'm summarising other people's arguments here, so any clumsiness in the framing is mine, not theirs.

## What happens to expertise when answers become cheap?

We deliberately didn't want to do the "will AI replace analysts?" episode. That debate has been running on autopilot for two years now and it produces roughly zero actionable insight for anyone actually doing the work.

The more interesting question is what practitioners need to understand if they want to use these tools responsibly *and* still be worth hiring in three years. Because the thing that changed isn't that AI can produce JavaScript, SQL or a tagging configuration. It's that it can produce all of them in a form confident enough that nobody feels the need to check.

Simo's central concern in the conversation was the growing temptation to skip the hard parts of learning. He's not romanticising suffering here. His point is rather mechanical in nature: Manually working through a problem is what builds the **mental model**, and the mental model is the only thing that lets you recognise when an output is wrong.

That distinction matters more than it used to. An incorrect answer that took someone three hours to produce spreads slowly through an organisation. An incorrect answer generated in four seconds, formatted nicely, and pasted straight into a Slack channel spreads at a completely different velocity.

> The skill that's appreciating in value isn't writing the code. It's being able to look at a plausible, well-formatted, confidently-worded answer and say "that's wrong, and here's why."

And you don't get that skill from reading about it. You get it from having been wrong yourself, repeatedly, in ways you had to debug manually.

## The fundamentals didn't go anywhere

Here's the part that I found genuinely reassuring, and it's a theme I keep running into - I even made [a very similar argument about measuring AI agents](https://gunnargriese.com/posts/measuring-agentic-chatbots/) earlier this year. Despite everything that has changed at the tooling layer, the underlying work of analytics is remarkably familiar.

Reliable measurement still depends on the same four things it always did:

- **Data quality**: Is what you're collecting actually what you think you're collecting?
- **Correct implementation**: Does the tracking fire when it should, with the right parameters, for the right users?
- **Sound technical foundations**: Is the infrastructure underneath it stable and understood?
- **Business context**: Do you know what the organisation is actually trying to achieve?

AI accelerates parts of this. It does not remove the need for good inputs or human validation. If anything, it raises the cost of bad inputs, because bad inputs now get processed, summarised and distributed much faster than before.

The conversation kept circling back to one principle in particular: **modelling and synthetic data cannot compensate indefinitely for weak real-world data.** You can paper over a gap for a while. You cannot paper over a foundation. Anyone who has watched a client's "conversion modelling" quietly absorb a broken consent implementation knows exactly what this looks like in practice.

## Where does AI actually earn its keep?

None of this makes Simo an AI sceptic, and I want to be careful not to flatten his position into "(old) man yells at chatbot." He was quite specific about where these tools genuinely pay off:

| Use case | Why it works well |
|---|---|
| Infrastructure optimisation | Well-defined problem space, verifiable outputs, tedious to do by hand |
| Anomaly detection | Pattern recognition at a scale humans can't sustain |
| Repetitive technical work | Boilerplate, migrations, refactors: low judgement, high volume |

The pattern across all three: AI should remove **low-value effort**, not low-effort thinking. Handing off the tedious parts is the entire point. Handing off the parts that build your judgement is how you end up unable to evaluate the output of the thing you handed off to.

That's the trade every one of us is making right now, usually without noticing we're making it.

## Why is analytics an organisational problem, not just a technical one?

About halfway through, the conversation broadened out from tooling into something else: how organisations actually use analytics.

For decades now, companies have invested heavily in analytics while structurally separating analysts from the teams making everyday business decisions. The data team sits over there. The decisions happen over here. Occasionally a ticket travels between them.

Steen raised the problem that follows from this setup, and he put it better than I would have: data becomes **"negotiable"** when stakeholders come looking for numbers that support a narrative they've already committed to. Once that dynamic sets in, the quality of your implementation almost stops mattering. You're simply not producing evidence anymore, you're producing ammunition.

Simo's argument is that analytics shouldn't function as an answer-producing department at all. Data becomes valuable when it's integrated into organisational processes and decision-making, not when it's delivered on request as a self-contained artefact.

Which, honestly, reframes the AI question entirely. If your analytics function was already just an answer factory, then yes: Something that produces answers faster and cheaper is genuinely threatening. If your analytics function is embedded in how decisions get made, AI is a tool that makes you better at it.

## So why bother with community when answers are on demand?

We closed the episode by connecting all of this back to why we started [AnalyticsDev.Net](https://analyticsdev.net) in the first place, and I'll admit the argument sounds counterintuitive at first.

In a world where information and answers are available on demand, you'd expect the value of communities, meetups and peer learning to collapse. Why sit in a session when you could just ask a model?

Our take: it goes the other way. When answers are abundant, the scarce things become judgement, context, and knowing which questions are worth asking. But none of those transfer well through documentation. They transfer through people who've made the mistake before are now telling you about it. Interaction and peer learning become *more* valuable, not less.

## Key takeaway

AI can make analytics faster, but speed alone does not create expertise. The practitioners who remain valuable will be the ones who combine AI fluency with strong technical foundations, critical thinking, sound data practices, and the ability to connect analytics to real organisational decisions.

Or put more bluntly: get very good at knowing when the machine is wrong.

Thanks to Simo for kicking off the series with us, and to Steen and Jomar for the conversation. If you want to catch future episodes or join the yearly meetup, everything lives over at [analyticsdev.net](https://analyticsdev.net/). And if you've got a topic or a strong opinion you'd like to defend on camera, feel free to reach out.

---
layout: page
title: Services - Signal Engineering, Measurement Infrastructure, Advisory
description: Senior measurement work for marketing, MarTech, and analytics teams - delivered by one practitioner with skin in the game
permalink: /services/
---

<div class="services-intro" style="max-width: 800px; margin-bottom: 3rem;">
  <h2 style="font-size: 2rem; margin-bottom: 1rem;">How I work with teams.</h2>
  <p style="font-size: 1.15rem; line-height: 1.7; color: var(--color-text-light);">Three categories of engagement for marketing, MarTech, and analytics teams that need senior measurement work - delivered by one practitioner with skin in the game. No account managers, no junior staffing, no slide-deck deliverables - just measurement infrastructure that ships.</p>
</div>

<div class="services-grid">

  <div class="service-card">
    <div class="service-header">
      <h2>Signal Design & Implementation</h2>
    </div>
    <div class="service-body">
      <p>Define what your business actually needs to measure, then build it properly. This starts with data contracts - explicit specifications of every event, parameter, and identifier - and ends with a production tracking implementation that holds up under engineering scrutiny.</p>

      <p>Most "tracking projects" fail because the upstream definitions were never agreed. I run this as a Signal Engineering exercise: business question, measurable signal, implementation, validation.</p>

      <h3>Core deliverables</h3>
      <ul>
        <li>Event schemas and data contracts as a first-class artifact</li>
        <li>GA4, Amplitude, or product-analytics implementation against the contract</li>
        <li>Server-side GTM where data quality, consent, or first-party context demands it</li>
        <li>Consent Mode v2 and privacy architecture that actually maps to your legal setup</li>
        <li>Schema validation and monitoring so the contract stays enforced after I leave</li>
      </ul>
    </div>
    <div class="service-footer">
      <a href="{{ '/contact' | relative_url }}" class="btn btn-secondary">Start a conversation</a>
    </div>
  </div>

  <div class="service-card">
    <div class="service-header">
      <h2>Measurement Infrastructure</h2>
    </div>
    <div class="service-body">
      <p>Build the pipelines that move signals from collection to activation. This is where most analytics setups stall: events are flowing, but nothing useful is happening downstream. The fix is real data engineering - not Data Studio dashboards on top of GA4.</p>

      <p>I design and build warehouse-native measurement systems on Google Cloud: BigQuery as the backbone, Dataform for transformation, server-side GTM for collection, and clean APIs into the activation surfaces (ad platforms, CDPs, ML models) that turn signals into outcomes.</p>

      <h3>Core deliverables</h3>
      <ul>
        <li>BigQuery + Dataform pipelines for marketing and product data</li>
        <li>GTM Server-Side infrastructure, including multi-region and data-residency setups</li>
        <li>Custom collection and enrichment logic in JavaScript, SQL, and Python</li>
        <li>Enhanced Conversions, offline conversions, value-based bidding signals</li>
        <li>AI-augmented analysis tooling - conversational analytics, automated validation, agent-ready data</li>
      </ul>
    </div>
    <div class="service-footer">
      <a href="{{ '/contact' | relative_url }}" class="btn btn-secondary">Start a conversation</a>
    </div>
  </div>

  <div class="service-card">
    <div class="service-header">
      <h2>Advisory, Audits & Training</h2>
    </div>
    <div class="service-body">
      <p>Independent technical advice for teams making big measurement decisions. I'm not a generalist strategy consultant - I'm the engineer your in-house team calls when the question is "is our setup actually doing what we think it's doing?"</p>

      <p>Audits are the most common entry point. They're structured, evidence-based, and end with a prioritized plan - not a 60-slide deck. Training engagements range from team workshops to half-year curricula, including the technical analytics course I teach at IHM Business School.</p>

      <h3>Core deliverables</h3>
      <ul>
        <li>Measurement audits with prioritized remediation plans</li>
        <li>Signal Engineering reviews - where are you on the maturity curve, what's the next step</li>
        <li>KPI and measurement framework development</li>
        <li>Team upskilling: GA4, GTM, server-side, BigQuery, modern measurement architecture</li>
        <li>Conference talks and executive workshops</li>
      </ul>
    </div>
    <div class="service-footer">
      <a href="{{ '/contact' | relative_url }}" class="btn btn-secondary">Start a conversation</a>
    </div>
  </div>

</div>

{% include testimonials.html %}

<!-- Full-width background section for better visual separation -->
<div style="background-color: #f8f9fa; margin: 4rem -2rem 0; padding: 3rem 2rem;">
  <section class="engagement-section">
    <h2 class="section-title">How we work together</h2>

  <div class="services-grid">

    <div class="service-card">
      <div class="service-header">
        <h3>Project-Based</h3>
      </div>
      <div class="service-body">
        <p>Fixed-scope engagements, 2-12 weeks. Implementations, audits, infrastructure builds, migrations. Clear deliverables, fixed price where possible, embedded delivery throughout.</p>

        <ul>
          <li>Signal design and implementation</li>
          <li>Technical audits and assessments</li>
          <li>Infrastructure builds and migrations</li>
        </ul>

        <p class="engagement-detail"><strong>Timeline:</strong> 2-12 weeks</p>
      </div>
      <div class="service-footer">
        <a href="{{ '/contact' | relative_url }}" class="btn btn-secondary">Start a project</a>
      </div>
    </div>

    <div class="service-card">
      <div class="service-header">
        <h3>Retainer</h3>
      </div>
      <div class="service-body">
        <p>Ongoing measurement partnership for teams that need senior measurement work without an in-house hire. Routed through 8-bit-sheep for contracting and continuity.</p>

        <ul>
          <li>Continuous measurement support</li>
          <li>Strategic advisory and roadmapping</li>
          <li>On-demand senior expertise</li>
        </ul>

        <p class="engagement-detail"><strong>Duration:</strong> Flexible monthly arrangements</p>
      </div>
      <div class="service-footer">
        <a href="{{ '/contact' | relative_url }}" class="btn btn-secondary">Discuss retainer options</a>
      </div>
    </div>

    <div class="service-card">
      <div class="service-header">
        <h3>Training & Workshops</h3>
      </div>
      <div class="service-body">
        <p>Half-day to multi-day programs for in-house teams. Conference speaking and executive workshops also available. Same depth as the consulting work, distilled for transfer.</p>

        <ul>
          <li>Half-day to multi-day programs</li>
          <li>Virtual or in-person delivery</li>
          <li>Conference speaking engagements</li>
        </ul>

        <p class="engagement-detail"><strong>Format:</strong> Custom curriculum development</p>
      </div>
      <div class="service-footer">
        <a href="{{ '/contact' | relative_url }}" class="btn btn-secondary">Book a training session</a>
      </div>
    </div>

  </div>

  <div class="cta-section" style="text-align: center; padding: 3rem 0;">
    <h3 style="text-align: center;">See if we're a fit</h3>
    <p style="text-align: center; margin-bottom: 2rem;">If you're considering a measurement engagement, the fastest way to find out is a 30-minute conversation.</p>
    <div style="text-align: center;">
      <a href="{{ '/contact' | relative_url }}" class="btn btn-primary btn-large">Start a conversation</a>
    </div>
  </div>
  </section>
</div>

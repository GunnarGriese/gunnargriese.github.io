---
layout: page
title: About - How I think about measurement
description: Independent measurement practitioner. Signal Engineering, embedded delivery, and a strong opinion about where analytics is going next.
permalink: /about/
---

<div class="about-hero">
  <div class="about-intro">
    <h2 class="section-title-left">An independent measurement practitioner. Embedded delivery, Signal Engineering, and a strong opinion about where analytics is going next.</h2>
    <p class="lead-text">I'm Gunnar Griese. I work with in-house teams as an embedded engineer for measurement - designing event schemas, building warehouse-native pipelines, and shipping the infrastructure that turns user behavior into signals modern systems can act on.</p>
    <p class="lead-text">Based in Copenhagen. Working internationally. Operating as an independent practitioner, with engagements routed through 8-bit-sheep.</p>
  </div>
</div>

<section class="about-section">
  <div class="content-grid">
    <div class="content-main">
      <h3>Three things I work from</h3>

      <p><strong>1. Measurement is engineering, not reporting.</strong> The interesting work happens upstream of the dashboard - in event design, data contracts, pipelines, and the systems that keep signals trustworthy as the product changes.</p>

      <p><strong>2. Marketing measurement is becoming a machine-to-machine problem.</strong> Ad platforms, predictive bidding models, and AI agents are now the primary consumers of marketing analytics output. Measurement built only for marketing dashboards doesn't feed these systems well - and the gap between teams who've made this shift and teams who haven't is widening fast.</p>

      <p><strong>3. Embedded beats advisory.</strong> The best measurement work happens when the engineer is in the same Slack channel, the same repo, and the same standup as the team. Slide-deck consulting is for problems that don't matter.</p>

      <p>I call this approach <strong>Signal Engineering</strong>, and it's the through-line in everything I do - implementations, audits, training, and the talks I give at Superweek, MeasureCamp, and the Digital Analytics Summit.</p>

      <h3>Background</h3>
      <p>Before going independent, I spent years at the leading digital analytics agencies in Germany (<strong>TRKKN</strong>) and Denmark (<strong>IIH Nordic</strong>), consulting enterprise clients on measurement architecture. I'm a <strong>Google Cloud Certified Professional Data Engineer</strong> and have expert experience across the Google measurement stack - GA4, GTM, server-side GTM, BigQuery, Dataform - with deep knowledge of Amplitude, Mixpanel, Segment, and Piwik Pro where they fit the problem better.</p>

      <h3>Beyond client work</h3>
      <p>I teach <strong>Technical Digital Analytics</strong> at IHM Business School in Malmö. I co-organize <strong>Kodbyen AI Sessions</strong>, a monthly practitioner meetup in Copenhagen for analytics and AI engineers. I write here on my blog and speak regularly at international conferences.</p>
    </div>

    <div class="content-sidebar">
      <div class="info-card">
        <h4>Primary stack</h4>
        <ul class="expertise-list">
          <li>Google Cloud Platform</li>
          <li>BigQuery</li>
          <li>Dataform</li>
          <li>Google Analytics 4</li>
          <li>GTM (web + server-side)</li>
          <li>JavaScript, SQL, Python</li>
        </ul>
      </div>

      <div class="info-card">
        <h4>Experienced with</h4>
        <ul class="expertise-list">
          <li>Amplitude</li>
          <li>Mixpanel</li>
          <li>Segment</li>
          <li>Piwik Pro</li>
          <li>Data Studio</li>
          <li>AI/LLM tooling for analytics</li>
        </ul>
      </div>

      <div class="info-card">
        <h4>Languages</h4>
        <ul class="language-list">
          <li><strong>German:</strong> Native</li>
          <li><strong>English:</strong> Fluent</li>
          <li><strong>Danish:</strong> Working Proficiency</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<div class="cta-section about-cta">
  <h3>See if we're a fit</h3>
  <p>If you're considering a measurement engagement - implementation, audit, infrastructure build, or training - the fastest way to find out is a 30-minute conversation.</p>
  <div class="cta-buttons">
    <a href="{{ '/contact' | relative_url }}" class="btn btn-primary btn-large">Start a conversation</a>
    <a href="{{ '/services' | relative_url }}" class="btn btn-secondary btn-large">Explore services</a>
  </div>
</div>

<style>
.about-hero {
  padding: 2rem 0 3rem;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 3rem;
}

.about-intro {
  max-width: 900px;
}

.section-title-left {
  text-align: left;
  font-size: 2rem;
  color: var(--color-text);
  margin-bottom: 1rem;
}

.lead-text {
  font-size: 1.25rem;
  line-height: 1.7;
  color: var(--color-text-light);
  margin-top: 1rem;
}

.about-section {
  margin-bottom: 4rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  margin-top: 2rem;
}

.content-main h3 {
  color: var(--color-text);
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.content-main h3:first-child {
  margin-top: 0;
}

.content-main p {
  margin-bottom: 1.25rem;
  line-height: 1.8;
  color: var(--color-text);
}

.content-sidebar {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-card {
  background: var(--color-bg-alt);
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid var(--color-border);
}

.info-card h4 {
  color: var(--color-text);
  margin-bottom: 1rem;
  font-size: 1.125rem;
}

.expertise-list,
.language-list {
  list-style: none;
  padding: 0;
}

.expertise-list li,
.language-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
}

.expertise-list li:last-child,
.language-list li:last-child {
  border-bottom: none;
}

.about-cta {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
  color: white;
  padding: 3rem 2rem;
  border-radius: 1rem;
  text-align: center;
  margin-top: 3rem;
}

.about-cta h3 {
  color: white;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.about-cta p {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2rem;
  font-size: 1.125rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-large {
  padding: 0.75rem 2rem;
  font-size: 1.125rem;
}

@media (max-width: 968px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .content-sidebar {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 640px) {
  .about-intro {
    padding: 0;
  }

  .lead-text {
    font-size: 1.125rem;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .btn-large {
    width: 100%;
  }
}
</style>

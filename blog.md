---
layout: page
title: Blog
description: I write about advanced digital analytics architecture – from server-side tracking and GA4/BigQuery integrations to privacy-first solutions and AI-powered workflows. This blog documents the technical patterns and enterprise-scale implementations you won't find in standard documentation. If you're looking to push beyond basic tracking and build sophisticated measurement systems that create competitive advantages, you're in the right place.
permalink: /blog/
---

<div class="blog-grid">
    {% for post in site.posts %}
    <article class="blog-tile">
        <a href="{{ post.url | relative_url }}" class="blog-tile-link">
            {% if post.image %}
            <div class="blog-tile-image">
                <img src="{{ post.image | relative_url }}" alt="{{ post.title }}">
            </div>
            {% else %}
            <div class="blog-tile-image blog-tile-placeholder">
                <div class="placeholder-content">
                    <span class="placeholder-icon">📝</span>
                </div>
            </div>
            {% endif %}

            <div class="blog-tile-content">
                <h2 class="blog-tile-title">{{ post.title }}</h2>
                <p class="blog-tile-excerpt">
                    {{ post.excerpt | strip_html | truncate: 150 }}
                </p>
                <div class="blog-tile-meta">
                    <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %-d, %Y" }}</time>
                    <span class="read-time">{{ post.content | number_of_words | divided_by: 200 | plus: 1 }} min read</span>
                </div>
            </div>
        </a>
    </article>
    {% endfor %}
</div>
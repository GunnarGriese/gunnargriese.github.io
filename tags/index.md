---
layout: page
title: Tags
description: Browse all blog posts by topic
permalink: /tags/
---

<div class="tags-index">
    <div class="tags-cloud">
        {% assign sorted_tags = site.tags | sort %}
        {% for tag in sorted_tags %}
            {% assign tag_name = tag[0] %}
            {% assign tag_posts = tag[1] %}
            <a href="{{ '/tags/' | append: tag_name | append: '/' | relative_url }}" class="tag-link">
                <span class="tag-name">{{ tag_name }}</span>
                <span class="tag-count">{{ tag_posts.size }}</span>
            </a>
        {% endfor %}
    </div>

    <div class="tags-list">
        <h2>All Tags</h2>
        {% assign sorted_tags = site.tags | sort %}
        {% for tag in sorted_tags %}
            {% assign tag_name = tag[0] %}
            {% assign tag_posts = tag[1] %}
            <div class="tag-section">
                <h3>
                    <a href="{{ '/tags/' | append: tag_name | append: '/' | relative_url }}">
                        {{ tag_name }} ({{ tag_posts.size }})
                    </a>
                </h3>
                <ul class="tag-posts">
                    {% for post in tag_posts limit:3 %}
                    <li>
                        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                        <time>{{ post.date | date: "%b %Y" }}</time>
                    </li>
                    {% endfor %}
                    {% if tag_posts.size > 3 %}
                    <li class="more-link">
                        <a href="{{ '/tags/' | append: tag_name | append: '/' | relative_url }}">
                            View all {{ tag_posts.size }} posts →
                        </a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        {% endfor %}
    </div>
</div>

<style>
.tags-cloud {
    margin-bottom: 3rem;
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
}

.tag-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f0f0f0;
    border-radius: 2rem;
    text-decoration: none;
    color: #333;
    transition: all 0.2s;
}

.tag-link:hover {
    background: #e0e0e0;
    transform: translateY(-2px);
}

.tag-name {
    font-weight: 500;
}

.tag-count {
    background: #333;
    color: white;
    padding: 0.125rem 0.5rem;
    border-radius: 1rem;
    font-size: 0.875rem;
}

.tags-list {
    margin-top: 2rem;
}

.tags-list h2 {
    margin-bottom: 2rem;
    text-align: center;
}

.tag-section {
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #eee;
}

.tag-section h3 {
    margin-bottom: 1rem;
}

.tag-section h3 a {
    text-decoration: none;
    color: #333;
}

.tag-section h3 a:hover {
    color: #0066cc;
}

.tag-posts {
    list-style: none;
    padding: 0;
}

.tag-posts li {
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.tag-posts li a {
    text-decoration: none;
    color: #555;
    flex: 1;
}

.tag-posts li a:hover {
    color: #0066cc;
}

.tag-posts time {
    color: #999;
    font-size: 0.875rem;
}

.more-link {
    margin-top: 0.5rem;
    font-weight: 500;
}

.more-link a {
    color: #0066cc !important;
}
</style>
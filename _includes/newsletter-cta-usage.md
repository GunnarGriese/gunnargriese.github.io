# Newsletter CTA Usage

To add an inline newsletter CTA within any blog post, simply add this liquid tag wherever you want the CTA to appear in your markdown:

```liquid
{% include newsletter-cta.html %}
```

## Example usage in a blog post:

```markdown
---
layout: post
title: "Your Blog Post Title"
---

## Introduction
Here's the beginning of your blog post...

Some interesting content here...

{% include newsletter-cta.html %}

## Next Section
More content continues here...
```

The CTA will:
- Display a styled call-to-action box with your brand colors
- When clicked, smoothly scroll the user to the main newsletter signup form at the bottom of the post
- Be fully responsive on mobile devices

You can place this CTA multiple times in a single post if desired, though once or twice per article is recommended for best user experience.
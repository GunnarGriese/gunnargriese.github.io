# Gunnar Griese - Personal Website

A professional consulting website built with Jekyll, designed for GitHub Pages deployment.

## Features

- Clean, professional design inspired by modern consulting sites
- Fully responsive layout
- Service offerings showcase
- Blog functionality
- Contact information
- SEO-friendly structure

## Local Development

1. Install Jekyll and Bundler:
```bash
gem install jekyll bundler
```

2. Install dependencies:
```bash
bundle install
```

3. Run the development server:
```bash
bundle exec jekyll serve
```

4. Open http://localhost:4000 in your browser

## Customization

### Update Personal Information

Edit `_config.yml` to update:
- Your name and title
- Email and social media links
- Site description
- URL (for production)

### Homepage Content

Edit `index.md` to customize:
- Hero section text
- Services offered
- About section content
- Call-to-action messages

### Adding Blog Posts

Create new posts in `_posts/` following the naming convention:
```
YYYY-MM-DD-post-title.md
```

#### Blog Post Images

Store blog post images in `/assets/images/blog/` and reference them in the post frontmatter:
```yaml
---
title: Your Post Title
date: YYYY-MM-DD HH:MM:SS +0200
image: /assets/images/blog/your-image.png
categories: [Category]
---
```

##### Image Generation Prompt for Blog Tiles

For consistent blog tile images, use this AI image generation prompt:

```
Create a clean, professional, and minimalist isometric 3D illustration for a blog preview tile. The central focus should be a technical metaphor for [YOUR TOPIC]. Use a composition of sleek icons, interconnected nodes, and subtle flow lines.

Aspect Ratio: 16:9 horizontal format (wide rectangular, not square)
Dimensions: 1200x675 pixels or 800x450 pixels

Style Constraints:

Colors: Use a primary background of #235495 (deep blue) and white. Use #dd973a (golden orange) strictly for highlights and accent lines.

Layout: The central graphic should be large and zoomed in, filling about 60-70% of the frame horizontally distributed across the wide canvas.

Aesthetics: Use a modern tech aesthetic with clean lines, soft gradients, and high-quality isometric perspective.

Background: A professional mix of solid color and subtle geometric patterns or diagonal accent lines in the brand colors.

Strict Rule: No text, no titles, and no labels anywhere in the image.
```

Replace `[YOUR TOPIC]` with your specific blog post subject (e.g., "GTM Server-Side Data Residency - Regional Load Balancers and Cloud DNS Geo-Routing").

### Styling

CSS styles are in `assets/css/main.css`. The design uses CSS variables for easy color scheme adjustments.

## GitHub Pages Deployment

### Option 1: Deploy to username.github.io

1. Create a repository named `[your-username].github.io`
2. Push this code to the main branch
3. Your site will be available at `https://[your-username].github.io`

### Option 2: Deploy to Custom Domain (gunnargriese.com)

1. Create repository `[your-username].github.io` or any project repository
2. Add a `CNAME` file with your domain:
```
gunnargriese.com
```
3. Configure DNS settings:
   - Add A records pointing to GitHub's IPs:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   - Or add CNAME record pointing to `[your-username].github.io`
4. Enable GitHub Pages in repository settings
5. Select source branch (usually main or gh-pages)

## Content Areas to Update

Before launching, update these placeholder sections:

1. **Profile Image**: Add your professional photo to `assets/images/profile.jpg`
2. **Services**: Update the services in `index.md` and `services.md`
3. **Experience**: Replace "[X years]" with your actual experience
4. **Expertise**: Replace "[your expertise]" with your specialization
5. **Value Proposition**: Replace "[your value proposition]" with your unique offering
6. **Contact Info**: Update email and social media links in `_config.yml`

## Directory Structure

```
.
├── _config.yml          # Site configuration
├── _layouts/            # Page templates
├── _includes/           # Reusable components
├── _posts/              # Blog posts
├── _sass/               # Sass partials (if using)
├── assets/
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript
│   └── images/         # Images
├── index.md            # Homepage
├── services.md         # Services page
├── contact.md          # Contact page
└── README.md           # This file
```

## To Do

- [x] Add About page
- [ ] Better transition on contact page
- [ ] Blog intro (why should people read it?, why am I writing it?, what am I writing about?)
- [ ] Add company logos to showcase past clients (Pyne, Sixt, Comwell, InboundCPH, Miss Mary of Sweden, Beely, Churney, DFDS, JFM, Profitmetrics, BLC, Supercell, etc.)

## License

This project is open source and available under the MIT License.
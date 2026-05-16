document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== Analytics: Link Click Tracking =====
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href]');
        if (!link) return;

        // Skip anchor links (handled by smooth scroll above)
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) return;

        // Get link text (fallback to href if no text)
        const linkText = link.textContent.trim() || href;

        // Determine link type and category
        let linkType = 'internal';
        let category = '';

        // Check for explicit data attributes (nav links, etc.)
        const dataType = link.getAttribute('data-analytics-type');
        const dataCategory = link.getAttribute('data-analytics-category');

        if (dataType) {
            linkType = dataType;
            category = dataCategory || '';
        } else {
            // Auto-detect link type if not explicitly set
            if (href && (href.includes('http') || href.startsWith('//'))) {
                const currentDomain = window.location.hostname;
                const linkDomain = new URL(href, window.location.origin).hostname;
                linkType = linkDomain === currentDomain ? 'internal' : 'external';
            }

            // Auto-detect category for specific links
            if (href.includes('/blog') || href.includes('/posts')) {
                category = 'blog';
            } else if (href.includes('/services')) {
                category = 'services';
            }
        }

        // Track link click (async, non-blocking)
        if (typeof Analytics !== 'undefined') {
            Analytics.trackLinkClick(href, linkText, linkType, category);
        }
    });

    // ===== Analytics: Scroll Depth Tracking =====
    if (typeof Analytics !== 'undefined' && 'IntersectionObserver' in window) {
        const scrollTracked = new Set();

        // Create sentinel elements at 25%, 50%, 75% of page height
        const thresholds = [25, 50, 75, 100];
        const sentinels = [];

        // Wait for full page load to calculate accurate heights
        window.addEventListener('load', function() {
            thresholds.forEach(threshold => {
                const sentinel = document.createElement('div');
                sentinel.style.cssText = 'position: absolute; height: 1px; width: 1px; pointer-events: none; visibility: hidden;';

                // Position sentinel at threshold percentage of document height
                const pageHeight = Math.max(
                    document.body.scrollHeight,
                    document.documentElement.scrollHeight,
                    document.body.offsetHeight,
                    document.documentElement.offsetHeight
                );
                const targetScrollPosition = (pageHeight * threshold) / 100;

                document.body.appendChild(sentinel);
                sentinel.style.top = targetScrollPosition + 'px';
                sentinel.setAttribute('data-scroll-threshold', threshold);

                sentinels.push(sentinel);
            });

            // Observe sentinels for intersection
            const observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const threshold = parseInt(entry.target.getAttribute('data-scroll-threshold'), 10);
                        // Fire only once per threshold per page load
                        if (!scrollTracked.has(threshold)) {
                            scrollTracked.add(threshold);
                            Analytics.trackScroll(threshold);
                        }
                    }
                });
            }, {
                threshold: 0
            });

            sentinels.forEach(function(sentinel) {
                observer.observe(sentinel);
            });
        });
    }
});
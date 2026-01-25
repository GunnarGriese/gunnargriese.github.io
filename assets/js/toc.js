document.addEventListener('DOMContentLoaded', function() {
    const tocContainer = document.getElementById('table-of-contents');
    if (!tocContainer) return;

    const postContent = document.querySelector('.post-content');
    if (!postContent) return;

    const headings = postContent.querySelectorAll('h2, h3, h4');
    if (headings.length === 0) {
        tocContainer.style.display = 'none';
        return;
    }

    const toc = document.createElement('div');
    toc.className = 'toc';

    const tocTitle = document.createElement('h3');
    tocTitle.className = 'toc-title';
    tocTitle.textContent = 'Table of Contents';
    toc.appendChild(tocTitle);

    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';

    headings.forEach(function(heading, index) {
        if (!heading.id) {
            const text = heading.textContent.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '-').toLowerCase();
            heading.id = 'heading-' + text + '-' + index;
        }

        const li = document.createElement('li');
        li.className = 'toc-item toc-' + heading.tagName.toLowerCase();

        const link = document.createElement('a');
        link.href = '#' + heading.id;
        link.textContent = heading.textContent;
        link.className = 'toc-link';

        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });

        li.appendChild(link);
        tocList.appendChild(li);
    });

    toc.appendChild(tocList);
    tocContainer.appendChild(toc);

    const tocLinks = toc.querySelectorAll('.toc-link');
    const observerOptions = {
        rootMargin: '-80px 0px -70% 0px',
        threshold: 0
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            const id = entry.target.getAttribute('id');
            const tocLink = toc.querySelector('a[href="#' + id + '"]');

            if (entry.isIntersecting) {
                tocLinks.forEach(function(link) {
                    link.classList.remove('active');
                });
                if (tocLink) {
                    tocLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    headings.forEach(function(heading) {
        observer.observe(heading);
    });

    function updateTocPosition() {
        const scrollY = window.pageYOffset;
        const navHeight = 60;

        if (scrollY > 100) {
            toc.classList.add('sticky');
            toc.style.top = (navHeight + 20) + 'px';
        } else {
            toc.classList.remove('sticky');
            toc.style.top = '';
        }
    }

    window.addEventListener('scroll', updateTocPosition);
    updateTocPosition();
});
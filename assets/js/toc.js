document.addEventListener('DOMContentLoaded', function() {
    const content = document.querySelector('.post-content');
    const toc = document.getElementById('toc');
    
    if (!content || !toc) return;

    // Find all h2 and h3 headings
    const headings = content.querySelectorAll('h2, h3');
    if (headings.length === 0) return;

    const tocList = document.createElement('ul');
    tocList.className = 'toc-list';
    let currentList = tocList;
    let previousLevel = 2;

    headings.forEach(heading => {
        const level = parseInt(heading.tagName.charAt(1));
        const text = heading.textContent;
        const slug = heading.id || text.toLowerCase().replace(/[^a-z0-9]+/g, '-');
        
        // Ensure heading has an ID for linking
        if (!heading.id) heading.id = slug;

        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.href = `#${slug}`;
        link.textContent = text;
        listItem.appendChild(link);

        // Handle nesting for h3 elements
        if (level > previousLevel) {
            const newList = document.createElement('ul');
            currentList.lastElementChild.appendChild(newList);
            currentList = newList;
        } else if (level < previousLevel) {
            currentList = tocList;
        }

        currentList.appendChild(listItem);
        previousLevel = level;
    });

    toc.appendChild(tocList);

    // Add click handler for smooth scrolling
    toc.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            e.preventDefault();
            const targetId = e.target.getAttribute('href').slice(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var slider = document.querySelector('.testimonials-slider');
    if (!slider) return;

    var track = slider.querySelector('.testimonials-track');
    var cards = Array.from(track.querySelectorAll('.testimonial-card'));
    var prevBtn = slider.querySelector('.testimonials-prev');
    var nextBtn = slider.querySelector('.testimonials-next');
    var total = cards.length;

    if (total <= 2 || !prevBtn || !nextBtn) return;

    // Clone last 2 cards to the beginning, first 2 to the end
    track.insertBefore(cards[total - 1].cloneNode(true), track.firstChild);
    track.insertBefore(cards[total - 2].cloneNode(true), track.firstChild);
    track.appendChild(cards[0].cloneNode(true));
    track.appendChild(cards[1].cloneNode(true));

    var allCards = track.querySelectorAll('.testimonial-card');
    var current = 2;
    var transitioning = false;

    function setPosition(index, animate) {
        if (!animate) {
            track.style.transition = 'none';
        }
        current = index;
        track.style.transform = 'translateX(-' + allCards[current].offsetLeft + 'px)';
        if (!animate) {
            track.offsetHeight; // force reflow
            track.style.transition = 'transform 0.5s ease';
        }
    }

    // Set initial position without animation
    setPosition(2, false);

    track.addEventListener('transitionend', function () {
        transitioning = false;
        // Snap from clone zone to real cards
        if (current >= total + 2) {
            setPosition(2, false);
        } else if (current <= 0) {
            setPosition(total, false);
        }
    });

    prevBtn.addEventListener('click', function () {
        if (transitioning) return;
        transitioning = true;
        setPosition(current - 1, true);
    });

    nextBtn.addEventListener('click', function () {
        if (transitioning) return;
        transitioning = true;
        setPosition(current + 1, true);
    });

    // Recalculate on resize
    window.addEventListener('resize', function () {
        setPosition(current, false);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var slider = document.querySelector('.testimonials-slider');
    if (!slider) return;

    var track = slider.querySelector('.testimonials-track');
    var cards = Array.from(track.querySelectorAll('.testimonial-card'));
    var prevBtn = slider.querySelector('.testimonials-prev');
    var nextBtn = slider.querySelector('.testimonials-next');
    var total = cards.length;

    if (total <= 1 || !prevBtn || !nextBtn) return;

    function getVisible() {
        return window.innerWidth <= 768 ? 1 : 2;
    }

    var visible = getVisible();

    // Clone cards for infinite loop: prepend last `visible` cards, append first `visible` cards
    function buildClones() {
        // Remove any existing clones
        track.querySelectorAll('[data-clone]').forEach(function (el) {
            el.remove();
        });

        visible = getVisible();

        for (var i = visible - 1; i >= 0; i--) {
            var clone = cards[total - 1 - i].cloneNode(true);
            clone.setAttribute('data-clone', 'true');
            track.insertBefore(clone, track.firstChild);
        }
        for (var j = 0; j < visible; j++) {
            var clone = cards[j].cloneNode(true);
            clone.setAttribute('data-clone', 'true');
            track.appendChild(clone);
        }
    }

    buildClones();

    var current = visible; // Start at the first real card
    var transitioning = false;

    function getAllCards() {
        return track.querySelectorAll('.testimonial-card');
    }

    function setPosition(index, animate) {
        var allCards = getAllCards();
        if (!animate) {
            track.style.transition = 'none';
        }
        current = index;
        track.style.transform = 'translateX(-' + allCards[current].offsetLeft + 'px)';
        if (!animate) {
            track.offsetHeight;
            track.style.transition = 'transform 0.5s ease';
        }
    }

    // Defer initial positioning to ensure layout is complete after cloning
    requestAnimationFrame(function () {
        setPosition(visible, false);
    });

    track.addEventListener('transitionend', function () {
        transitioning = false;
        if (current >= total + visible) {
            setPosition(visible, false);
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

    var resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            var newVisible = getVisible();
            if (newVisible !== visible) {
                buildClones();
                current = newVisible;
                setPosition(current, false);
            } else {
                setPosition(current, false);
            }
        }, 150);
    });
});

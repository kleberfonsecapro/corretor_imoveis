document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('presPrev');
    const nextBtn = document.getElementById('presNext');
    const counter = document.getElementById('presCounter');
    const progressBars = document.querySelectorAll('.pres-progress-bar');
    const dots = document.querySelectorAll('.pres-dot');
    let current = 0;
    const total = slides.length;
    let autoplayTimer;

    function updateSlide(index) {
        slides.forEach((s, i) => {
            s.classList.toggle('active', i === index);
        });
        progressBars.forEach((bar, i) => {
            bar.classList.toggle('active', i === index);
        });
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
        counter.textContent = `${String(index + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
        resetAutoplay();
    }

    function nextSlide() {
        current = (current + 1) % total;
        updateSlide(current);
    }

    function prevSlide() {
        current = (current - 1 + total) % total;
        updateSlide(current);
    }

    function startAutoplay() {
        stopAutoplay();
        autoplayTimer = setInterval(nextSlide, 7000);
    }

    function stopAutoplay() {
        if (autoplayTimer) clearInterval(autoplayTimer);
    }

    function resetAutoplay() {
        stopAutoplay();
        startAutoplay();
    }

    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);

    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            current = i;
            updateSlide(current);
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            nextSlide();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            prevSlide();
        }
    });

    slides.forEach(s => {
        s.addEventListener('mouseenter', stopAutoplay);
        s.addEventListener('mouseleave', startAutoplay);
    });

    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) nextSlide();
            else prevSlide();
        }
    }, { passive: true });

    startAutoplay();
});

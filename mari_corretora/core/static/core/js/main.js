(function () {
  'use strict';

  /* Preloader */
  const preloader = document.getElementById('preloader');
  if (preloader) {
    window.addEventListener('load', function () {
      setTimeout(function () {
        preloader.classList.add('hidden');
      }, 800);
    });
  }

  /* Header scroll effect */
  const header = document.getElementById('header');
  let lastScroll = 0;

  function handleScroll() {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 80) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
  }

  window.addEventListener('scroll', handleScroll, { passive: true });

  /* Mobile menu */
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');
  const navLinks = document.querySelectorAll('.nav-link');

  function toggleMenu() {
    hamburger.classList.toggle('active');
    nav.classList.toggle('active');
    document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
  }

  function closeMenu() {
    hamburger.classList.remove('active');
    nav.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (hamburger) {
    hamburger.addEventListener('click', toggleMenu);
  }

  navLinks.forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  /* Active nav link on scroll */
  function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.pageYOffset + 150;

    sections.forEach(function (section) {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(function (link) {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveNavLink, { passive: true });

  /* Carousel */
  const track = document.getElementById('carouselTrack');
  const prevBtn = document.getElementById('carouselPrev');
  const nextBtn = document.getElementById('carouselNext');
  const dotsContainer = document.getElementById('carouselDots');

  if (track) {
    const slides = track.querySelectorAll('.carousel-slide');
    const totalSlides = slides.length;
    let currentIndex = 0;
    let autoplayInterval;

    function createDots() {
      if (!dotsContainer) return;
      dotsContainer.innerHTML = '';
      for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('button');
        dot.classList.add('carousel-dot');
        dot.setAttribute('aria-label', 'Ir para slide ' + (i + 1));
        if (i === 0) dot.classList.add('active');
        dot.addEventListener('click', function () {
          goToSlide(i);
          resetAutoplay();
        });
        dotsContainer.appendChild(dot);
      }
    }

    function goToSlide(index) {
      currentIndex = index;
      if (currentIndex < 0) currentIndex = totalSlides - 1;
      if (currentIndex >= totalSlides) currentIndex = 0;
      track.style.transform = 'translateX(-' + (currentIndex * 100) + '%)';

      const dots = dotsContainer.querySelectorAll('.carousel-dot');
      dots.forEach(function (dot, i) {
        dot.classList.toggle('active', i === currentIndex);
      });
    }

    function nextSlide() {
      goToSlide(currentIndex + 1);
    }

    function prevSlide() {
      goToSlide(currentIndex - 1);
    }

    function startAutoplay() {
      autoplayInterval = setInterval(nextSlide, 5000);
    }

    function resetAutoplay() {
      clearInterval(autoplayInterval);
      startAutoplay();
    }

    createDots();

    if (prevBtn) prevBtn.addEventListener('click', function () { prevSlide(); resetAutoplay(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { nextSlide(); resetAutoplay(); });

    startAutoplay();

    /* Pause autoplay on hover */
    const container = track.closest('.carousel-container');
    if (container) {
      container.addEventListener('mouseenter', function () {
        clearInterval(autoplayInterval);
      });
      container.addEventListener('mouseleave', function () {
        startAutoplay();
      });
    }

    /* Touch support */
    let startX = 0;
    let isDragging = false;

    track.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX;
      isDragging = true;
      clearInterval(autoplayInterval);
    }, { passive: true });

    track.addEventListener('touchend', function (e) {
      if (!isDragging) return;
      const endX = e.changedTouches[0].clientX;
      const diff = startX - endX;
      if (Math.abs(diff) > 50) {
        if (diff > 0) nextSlide();
        else prevSlide();
      }
      isDragging = false;
      startAutoplay();
    }, { passive: true });
  }

  /* Hero background slideshow */
  const heroSlides = document.querySelectorAll('.hero-bg-slide');
  if (heroSlides.length > 1) {
    let heroCurrent = 0;
    setInterval(function () {
      heroSlides.forEach(function (s) { s.classList.remove('active'); });
      heroCurrent = (heroCurrent + 1) % heroSlides.length;
      heroSlides[heroCurrent].classList.add('active');
    }, 6000);
  }

  /* Scroll to top button */
  const scrollBtn = document.getElementById('scrollToTop');
  if (scrollBtn) {
    window.addEventListener('scroll', function () {
      if (window.pageYOffset > 500) {
        scrollBtn.classList.add('visible');
      } else {
        scrollBtn.classList.remove('visible');
      }
    }, { passive: true });
  }

  /* Smooth scroll for anchor links */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = header ? header.offsetHeight : 70;
        const targetPos = target.offsetTop - headerHeight;
        window.scrollTo({
          top: targetPos,
          behavior: 'smooth'
        });
      }
    });
  });

  /* Animated numbers (stats) */
  const statNumbers = document.querySelectorAll('.stat-number');
  if (statNumbers.length > 0) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-target'), 10);
          if (!target) return;
          let current = 0;
          const increment = Math.ceil(target / 60);
          const timer = setInterval(function () {
            current += increment;
            if (current >= target) {
              el.textContent = target;
              clearInterval(timer);
            } else {
              el.textContent = current;
            }
          }, 25);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(function (num) {
      if (num.getAttribute('data-target')) {
        observer.observe(num);
      }
    });
  }

  /* Parallax effect on hero */
  const hero = document.querySelector('.hero');
  if (hero) {
    window.addEventListener('scroll', function () {
      const scrollPos = window.pageYOffset;
      const slides = hero.querySelectorAll('.hero-bg-slide');
      slides.forEach(function (slide) {
        slide.style.transform = 'translateY(' + (scrollPos * 0.3) + 'px)';
      });
    }, { passive: true });
  }
})();

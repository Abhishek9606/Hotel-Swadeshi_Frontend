document.addEventListener('DOMContentLoaded', function() {
    const reveal1 = document.querySelector('.hero-reveal-1');
    const reveal2 = document.querySelector('.hero-reveal-2');
    const reveal3 = document.querySelector('.hero-reveal-3');
    const reveal4 = document.querySelector('.hero-reveal-4');

    // Step 1: "WELCOME TO" on page load
    setTimeout(() => reveal1?.classList.add('visible'), 400);

    let titleShown = false;
    let taglineShown = false;

    function handleHeroScroll() {
        const y = window.scrollY;

        if (!titleShown && y > 25) {
            reveal2?.classList.add('visible');
            titleShown = true;
        }

        if (!taglineShown && y > 90) {
            reveal3?.classList.add('visible');
            taglineShown = true;
        }

        if (taglineShown) {
            reveal4?.classList.add('visible');
        }
    }

    window.addEventListener('scroll', handleHeroScroll, { passive: true });

    // Quote & CTA scroll animations
    const fadeElements = document.querySelectorAll('.fade-in');

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.15 });

    fadeElements.forEach(element => observer.observe(element));
});

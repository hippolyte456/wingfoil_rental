// Main JavaScript file

document.addEventListener('DOMContentLoaded', function () {
    // Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            const icon = navToggle.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Close mobile menu when clicking outside
    document.addEventListener('click', function (event) {
        if (navLinks && navLinks.classList.contains('active') && !event.target.closest('nav')) {
            navLinks.classList.remove('active');
            const icon = navToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Add scroll indicator to hero section
    const heroSection = document.querySelector('.hero');
    if (heroSection) {
        const scrollIndicator = document.createElement('div');
        scrollIndicator.className = 'scroll-indicator';
        scrollIndicator.innerHTML = `
            <span>Scroll Down</span>
            <div class="mouse"></div>
        `;
        heroSection.appendChild(scrollIndicator);
    }

    // Add typing animation to specific elements if they exist
    const typingElements = document.querySelectorAll('.typing-animation');
    if (typingElements.length > 0) {
        typingElements.forEach(element => {
            const text = element.textContent;
            element.textContent = '';
            element.style.width = '0';

            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 100);
                }
            };

            typeWriter();
        });
    }

    // Add gradient text animation to elements with class 'gradient-text'
    const gradientElements = document.querySelectorAll('.gradient-text');
    if (gradientElements.length > 0) {
        gradientElements.forEach(element => {
            // The CSS animation is already applied via the class
        });
    }

    // Add feature icon animation
    const featureIcons = document.querySelectorAll('.feature-card i');
    if (featureIcons.length > 0) {
        featureIcons.forEach(icon => {
            icon.classList.add('feature-icon-animation');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 70, // Adjust for header height
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                if (navLinks && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    const icon = navToggle.querySelector('i');
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });
    });

    // Page transition effect for internal links
    document.querySelectorAll('a:not([href^="#"]):not([href^="http"]):not([href^="mailto"])').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href && !href.startsWith('#') && !href.startsWith('http')) {
                e.preventDefault();

                const transition = document.createElement('div');
                transition.className = 'page-transition exit';
                document.body.appendChild(transition);

                setTimeout(() => {
                    window.location.href = href;
                }, 500);
            }
        });
    });

    // Check if we're coming from another page and show enter animation
    if (performance.navigation.type === 1 || document.referrer.includes(window.location.hostname)) {
        const transition = document.createElement('div');
        transition.className = 'page-transition enter';
        document.body.appendChild(transition);

        setTimeout(() => {
            transition.remove();
        }, 500);
    }

    // Parallax effect for hero section
    const heroImage = document.querySelector('.hero-image');
    if (heroImage) {
        window.addEventListener('mousemove', function (e) {
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;

            heroImage.style.transform = `translate(${x * 20 - 10}px, ${y * 20 - 10}px)`;

            // Also move floating elements for extra effect
            const floatingElements = document.querySelectorAll('.floating-element');
            floatingElements.forEach((el, index) => {
                const factor = (index + 1) * 5;
                el.style.transform = `translate(${x * factor - factor / 2}px, ${y * factor - factor / 2}px) rotate(${x * y * 20}deg)`;
            });
        });
    }

    // Add active class to current page in navigation
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks2 = document.querySelectorAll('.nav-links a');

    navLinks2.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (currentPage === linkPage || (currentPage === '' && linkPage === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// Add a class to animate elements when they come into view (fallback if AOS doesn't work)
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.bottom >= 0
    );
}

function handleScrollAnimation() {
    const elements = document.querySelectorAll('.animate-on-scroll');

    elements.forEach(element => {
        if (isElementInViewport(element)) {
            element.classList.add('is-visible');
        }
    });
}

// Listen for scroll events
window.addEventListener('scroll', handleScrollAnimation);
window.addEventListener('resize', handleScrollAnimation);
window.addEventListener('load', handleScrollAnimation); 
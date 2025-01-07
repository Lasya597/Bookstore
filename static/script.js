// Script.js for Online Book Store

// Smooth Scrolling for Navigation Links
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function (event) {
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
            event.preventDefault();
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Form Validation for the Contact Us Page
const contactForm = document.querySelector('form');
if (contactForm) {
    contactForm.addEventListener('submit', function (event) {
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();

        if (!name || !email || !message) {
            alert('Please fill out all fields before submitting the form.');
            event.preventDefault();
        } else if (!validateEmail(email)) {
            alert('Please enter a valid email address.');
            event.preventDefault();
        } else {
            alert('Thank you for contacting us! We will get back to you soon.');
        }
    });
}

// Email Validation Function
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// Highlight Active Navigation Link
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function () {
        document.querySelectorAll('nav a').forEach(navLink => navLink.classList.remove('active'));
        this.classList.add('active');
    });
});

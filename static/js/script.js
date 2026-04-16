// ============================================
// LANGUAGE SWITCHER
// ============================================

// Wait for i18n to be initialized
function waitForI18n(callback, attempts = 0) {
    if (typeof i18n !== 'undefined' && i18n.initialized) {
        callback();
    } else if (attempts < 50) {
        setTimeout(() => waitForI18n(callback, attempts + 1), 50);
    } else {
        console.warn('i18n initialization timeout');
        callback();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    waitForI18n(function() {
        const langToggle = document.getElementById('langToggle');
        const langDropdown = document.getElementById('langDropdown');
        const langOptions = document.querySelectorAll('.lang-option');
        const currentLangSpan = document.getElementById('currentLang');

        if (langToggle && langDropdown) {
            // Toggle dropdown
            langToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                langDropdown.classList.toggle('active');
            });

            // Language option selection
            langOptions.forEach(option => {
                option.addEventListener('click', (e) => {
                    e.preventDefault();
                    const lang = option.getAttribute('data-lang');
                    i18n.setLanguage(lang);
                    currentLangSpan.textContent = lang.toUpperCase();
                    langDropdown.classList.remove('active');
                    
                    // Update active state
                    langOptions.forEach(opt => opt.classList.remove('active'));
                    option.classList.add('active');
                    
                    // Analytics
                    if (typeof analytics !== 'undefined') {
                        analytics.trackEvent('language_changed', { language: lang });
                    }
                });
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.language-switcher')) {
                    langDropdown.classList.remove('active');
                }
            });

            // Set initial active language
            const initialLang = i18n.currentLanguage;
            currentLangSpan.textContent = initialLang.toUpperCase();
            document.querySelector(`[data-lang="${initialLang}"]`)?.classList.add('active');
        }
    });
});

// ============================================
// MOBILE MENU & LANGUAGE SWITCHER INTERACTION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Toggle hamburger menu
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Close menu when a link is clicked
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = event.target.closest('.nav-container');
        if (!isClickInsideNav && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });
});

// ============================================
// SCROLL ANIMATIONS
// ============================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe sections for animation
document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.about, .focus-areas, .featured-project, .join-movement, .founder-message');
    sections.forEach(section => {
        observer.observe(section);
    });

    // Observe cards
    const cards = document.querySelectorAll('.focus-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        setTimeout(() => {
            observer.observe(card);
        }, index * 100);
    });
});

// ============================================
// SMOOTH SCROLL BEHAVIOR
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ============================================
// NAVBAR SCROLL EFFECT
// ============================================

const navbar = document.querySelector('.navbar');
let lastScrollTop = 0;

window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Add shadow on scroll
    if (scrollTop > 10) {
        navbar.style.boxShadow = '0 8px 30px rgba(0, 0, 0, 0.12)';
    } else {
        navbar.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// ============================================
// BUTTON CLICK HANDLERS & MODALS
// ============================================

// Modal Functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside content
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        const modalId = event.target.id;
        closeModal(modalId);
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            closeModal(modal.id);
        });
    }
});

// Form submission
function submitForm(formId, modalId) {
    const form = document.getElementById(formId);
    if (form) {
        // Special validation for joinForm - check cover letter
        if (formId === 'joinForm') {
            const coverLetterText = form.querySelector('input[name="cover_letter_text"], textarea[name="cover_letter_text"]');
            const coverLetterFile = form.querySelector('input[name="cover_letter_file"]');
            
            // Check if either text or file is provided
            const hasText = coverLetterText && coverLetterText.value.trim().length > 0;
            const hasFile = coverLetterFile && coverLetterFile.files.length > 0;
            
            if (!hasText && !hasFile) {
                showNotification('❌ Please provide a cover letter (type text or upload file).');
                return;
            }
        }
        
        // Standard validation
        if (!form.checkValidity()) {
            showNotification('❌ Please fill in all required fields correctly.');
            return;
        }
        
        const formData = new FormData(form);
        
        // Get file info if exists
        const fileInputs = form.querySelectorAll('input[type="file"]');
        let fileInfo = {};
        fileInputs.forEach(input => {
            if (input.files.length > 0) {
                fileInfo[input.name] = {
                    filename: input.files[0].name,
                    size: input.files[0].size,
                    type: input.files[0].type
                };
            }
        });
        
        // Convert to object for logging
        const data = Object.fromEntries(formData);
        
        // Add file info
        if (Object.keys(fileInfo).length > 0) {
            data.files = fileInfo;
        }
        
        // Log to console (in production, send to backend)
        console.log('✓ Form submitted:', data);
        console.log('📎 Files attached:', fileInfo);
        
        // Show success notification
        const successMsg = formId === 'joinForm' 
            ? '✓ Application submitted successfully! We will review and contact you soon.' 
            : '✓ Form submitted successfully! We will contact you soon.';
        showNotification(successMsg);
        
        // Reset form
        form.reset();
        resetFileInputs(form);
        
        // Close modal
        closeModal(modalId);
        
        // Track in analytics
        if (typeof analytics !== 'undefined') {
            analytics.trackEvent('form_submitted', { form_type: formId, files_count: Object.keys(fileInfo).length });
        }
    }
}

// Reset file inputs display
function resetFileInputs(form) {
    const fileInputs = form.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        const fileNameSpan = input.nextElementSibling;
        if (fileNameSpan && fileNameSpan.classList.contains('file-name')) {
            fileNameSpan.textContent = 'No file chosen';
        }
    });
}

// Handle file input display
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const tabName = btn.getAttribute('data-tab');
            
            // Remove active from all buttons and tabs
            tabBtns.forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            
            // Add active to clicked button and corresponding tab
            btn.classList.add('active');
            const tabContent = document.getElementById(tabName);
            if (tabContent) {
                tabContent.classList.add('active');
            }
        });
    });

    // File input handling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const fileNameSpan = this.nextElementSibling;
            if (fileNameSpan && fileNameSpan.classList.contains('file-name')) {
                if (this.files.length > 0) {
                    const file = this.files[0];
                    const sizeMB = (file.size / 1024 / 1024).toFixed(2);
                    fileNameSpan.textContent = `✓ ${file.name} (${sizeMB} MB)`;
                    fileNameSpan.style.color = 'var(--accent-green)';
                } else {
                    fileNameSpan.textContent = 'No file chosen';
                    fileNameSpan.style.color = 'var(--text-light)';
                }
            }
        });

        // Make parent div clickable
        const fileUpload = input.closest('.file-upload');
        if (fileUpload) {
            fileUpload.addEventListener('click', () => input.click());
            fileUpload.addEventListener('dragover', (e) => {
                e.preventDefault();
                fileUpload.style.background = 'rgba(102, 204, 51, 0.15)';
            });
            fileUpload.addEventListener('dragleave', () => {
                fileUpload.style.background = 'rgba(102, 204, 51, 0.05)';
            });
            fileUpload.addEventListener('drop', (e) => {
                e.preventDefault();
                fileUpload.style.background = 'rgba(102, 204, 51, 0.05)';
                if (e.dataTransfer.files.length > 0) {
                    input.files = e.dataTransfer.files;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        }
    });
});

// Hero Button Handlers
document.addEventListener('DOMContentLoaded', function() {
    // Wait for i18n to initialize
    setTimeout(() => {
        const buttons = document.querySelectorAll('.cta-buttons .btn, .movement-buttons .btn');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const buttonText = this.textContent.trim();
                
                // Ripple effect
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');
                this.appendChild(ripple);
                
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                
                setTimeout(() => ripple.remove(), 600);
                
                // Open appropriate modal based on button text
                if (buttonText.includes('Join') || buttonText.includes('Volunteer')) {
                    openModal('joinModal');
                } else if (buttonText.includes('Explore') || buttonText.includes('Projects')) {
                    openModal('projectsModal');
                } else if (buttonText.includes('Partner')) {
                    openModal('partnerModal');
                }
                
                // Analytics
                if (typeof analytics !== 'undefined') {
                    analytics.trackEvent('button_clicked', { button_text: buttonText });
                }
            });
        });
    }, 100);
});


// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #1e4226, #66cc33);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease forwards;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        max-width: 300px;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// ============================================
// ADD ANIMATION STYLES TO HEAD
// ============================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out forwards;
        background: rgba(255, 255, 255, 0.7);
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        from {
            transform: scale(0);
            opacity: 1;
        }
        to {
            transform: scale(1);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ============================================
// SCROLL COUNTER FOR STATS
// ============================================

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// ============================================
// ACTIVE NAV LINK HIGHLIGHTING
// ============================================

window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Add active styling
const navActiveStyle = document.createElement('style');
navActiveStyle.textContent = `
    .nav-link.active::after {
        width: 100%;
    }
`;
document.head.appendChild(navActiveStyle);

// ============================================
// FORM VALIDATION HELPER
// ============================================

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateForm(formData) {
    const errors = [];
    
    if (!formData.name || formData.name.trim().length < 2) {
        errors.push('Please enter a valid name');
    }
    
    if (!formData.email || !validateEmail(formData.email)) {
        errors.push('Please enter a valid email');
    }
    
    if (!formData.message || formData.message.trim().length < 10) {
        errors.push('Please enter a message with at least 10 characters');
    }
    
    return errors;
}

// ============================================
// PAGE LOAD OPTIMIZATION
// ============================================

window.addEventListener('load', () => {
    // Log performance metrics
    const perfData = window.performance.timing;
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log('Page load time:', pageLoadTime, 'ms');
});

// ============================================
// ACCESSIBILITY IMPROVEMENTS
// ============================================

// Keyboard navigation support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const navMenu = document.querySelector('.nav-menu');
        const hamburger = document.querySelector('.hamburger');
        if (navMenu && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    }
});

// Focus visible styling for keyboard navigation
document.addEventListener('focusin', (e) => {
    if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') {
        e.target.style.outline = `2px solid #66cc33`;
        e.target.style.outlineOffset = '2px';
    }
});

document.addEventListener('focusout', (e) => {
    if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') {
        e.target.style.outline = 'none';
    }
});

console.log('EcoHub Group - Let\'s build a sustainable future together!');

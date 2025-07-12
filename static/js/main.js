// Main JavaScript for Skill Swap Platform - Performance Optimized

// Performance cache
const performanceCache = new Map();
const requestCache = new Map();

// Request deduplication
function deduplicateRequest(key, requestFn) {
    if (requestCache.has(key)) {
        return requestCache.get(key);
    }
    
    const promise = requestFn().finally(() => {
        requestCache.delete(key);
    });
    
    requestCache.set(key, promise);
    return promise;
}

// Optimized DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

function initializeApp() {
    // Initialize core features
    initializeTooltips();
    initializeFormValidation();
    initializeSearch();
    initializeSkillManagement();
    initializeRating();
    initializeNotifications();
    initializeLazyLoading();
    initializeVirtualScrolling();
    initializeServiceWorker();
    
    // Performance optimizations
    optimizeImages();
    preloadCriticalData();
    
    // Add fade-in animation to cards
    animateCards();
}

/**
 * Initialize Service Worker for caching
 */
function initializeServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('Service Worker registered:', registration);
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    }
}

/**
 * Preload critical data
 */
function preloadCriticalData() {
    // Preload skills data
    deduplicateRequest('skills', () => 
        fetch('/api/skills')
            .then(response => response.json())
            .then(data => {
                performanceCache.set('skills', data);
                return data;
            })
    );
    
    // Preload user skills if logged in
    const userId = document.body.dataset.userId;
    if (userId) {
        deduplicateRequest(`user_skills_${userId}`, () =>
            fetch(`/api/user_skills/${userId}`)
                .then(response => response.json())
                .then(data => {
                    performanceCache.set(`user_skills_${userId}`, data);
                    return data;
                })
        );
    }
}

/**
 * Initialize Bootstrap tooltips with performance optimization
 */
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length === 0) return;
    
    // Use requestAnimationFrame for better performance
    requestAnimationFrame(() => {
        tooltipTriggerList.forEach(tooltipTriggerEl => {
            new bootstrap.Tooltip(tooltipTriggerEl, {
                trigger: 'hover focus',
                delay: { show: 500, hide: 100 }
            });
        });
    });
}

/**
 * Initialize form validation with optimized event handling
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    if (forms.length === 0) return;
    
    forms.forEach(form => {
        // Debounced validation
        const debouncedValidation = debounce((field) => {
            if (field.checkValidity()) {
                field.classList.remove('is-invalid');
                field.classList.add('is-valid');
            } else {
                field.classList.remove('is-valid');
                field.classList.add('is-invalid');
            }
        }, 300);
        
        // Add event listeners efficiently
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', () => debouncedValidation(field), { passive: true });
        });
        
        // Form submission with loading state
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    showLoading(submitBtn);
                }
            }
            form.classList.add('was-validated');
        });
    });
    
    // Special handling for registration form
    const registrationForm = document.querySelector('form[action*="register"]');
    if (registrationForm) {
        const passwordField = registrationForm.querySelector('#password');
        const confirmPasswordField = registrationForm.querySelector('#confirm_password');
        
        if (passwordField && confirmPasswordField) {
            const validatePasswordMatch = debounce(() => {
                const password = passwordField.value;
                const confirmPassword = confirmPasswordField.value;
                
                if (confirmPassword && password !== confirmPassword) {
                    confirmPasswordField.setCustomValidity('Passwords do not match');
                    confirmPasswordField.classList.add('is-invalid');
                } else {
                    confirmPasswordField.setCustomValidity('');
                    confirmPasswordField.classList.remove('is-invalid');
                }
            }, 300);
            
            passwordField.addEventListener('input', validatePasswordMatch, { passive: true });
            confirmPasswordField.addEventListener('input', validatePasswordMatch, { passive: true });
        }
    }
}

/**
 * Initialize search functionality with performance optimizations
 */
function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;
    
    const searchForm = searchInput.closest('form');
    
    // Optimized search with caching
    const debouncedSearch = debounce((query) => {
        if (query.length < 2) return;
        
        const cacheKey = `search_${query}`;
        if (performanceCache.has(cacheKey)) {
            displaySearchSuggestions(performanceCache.get(cacheKey));
            return;
        }
        
        // Could implement real-time search suggestions here
        console.log('Searching for:', query);
    }, 300);
    
    searchInput.addEventListener('input', (e) => {
        debouncedSearch(e.target.value.trim());
    }, { passive: true });
    
    // Enhanced keyboard navigation
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (searchForm) {
                searchForm.submit();
            }
        }
    });
    
    // Clear search functionality
    const clearSearchBtn = document.querySelector('.clear-search');
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            searchInput.value = '';
            const availabilitySelect = document.querySelector('select[name="availability"]');
            if (availabilitySelect) {
                availabilitySelect.value = '';
            }
            if (searchForm) {
                searchForm.submit();
            }
        });
    }
}

/**
 * Initialize skill management with performance optimizations
 */
function initializeSkillManagement() {
    // Get cached skills data
    const skillsData = performanceCache.get('skills') || [];
    
    // Optimized skill autocomplete
    function setupSkillAutocomplete(input, skills) {
        if (!input || !skills.length) return;
        
        const debouncedAutocomplete = debounce((value) => {
            const suggestions = skills
                .filter(skill => skill.name.toLowerCase().includes(value.toLowerCase()))
                .slice(0, 10);
            
            updateDatalist(input, suggestions);
        }, 200);
        
        input.addEventListener('input', (e) => {
            const value = e.target.value;
            if (value.length >= 2) {
                debouncedAutocomplete(value);
            }
        }, { passive: true });
    }
    
    function updateDatalist(input, suggestions) {
        // Remove existing datalist
        const existingDatalist = document.querySelector(`#${input.getAttribute('list')}`);
        if (existingDatalist) {
            existingDatalist.remove();
        }
        
        if (suggestions.length > 0) {
            const datalist = document.createElement('datalist');
            const listId = 'skills-list-' + Math.random().toString(36).substr(2, 9);
            datalist.id = listId;
            
            const fragment = document.createDocumentFragment();
            suggestions.forEach(skill => {
                const option = document.createElement('option');
                option.value = skill.name || skill;
                fragment.appendChild(option);
            });
            
            datalist.appendChild(fragment);
            input.setAttribute('list', listId);
            input.parentNode.appendChild(datalist);
        }
    }
    
    // Initialize autocomplete for existing skill inputs
    const skillInputs = document.querySelectorAll('.skill-input');
    skillInputs.forEach(input => {
        setupSkillAutocomplete(input, skillsData);
    });
    
    // Dynamic skill management with event delegation
    function setupSkillManagement(containerId, inputName, buttonId) {
        const container = document.querySelector(containerId);
        const addButton = document.querySelector(buttonId);
        
        if (!container || !addButton) return;
        
        addButton.addEventListener('click', () => {
            const skillItem = createSkillItem(inputName, skillsData);
            container.appendChild(skillItem);
            
            // Focus on new input
            const newInput = skillItem.querySelector('.skill-input');
            newInput.focus();
        });
        
        // Event delegation for remove buttons
        container.addEventListener('click', (e) => {
            if (e.target.matches('.remove-skill') || e.target.closest('.remove-skill')) {
                e.preventDefault();
                
                const skillItem = e.target.closest('.skill-item');
                const skillItems = container.querySelectorAll('.skill-item');
                
                if (skillItems.length > 1) {
                    skillItem.style.animation = 'fadeOut 0.3s ease-out';
                    setTimeout(() => skillItem.remove(), 300);
                } else {
                    const input = skillItem.querySelector('input');
                    if (input) {
                        input.value = '';
                        input.focus();
                    }
                }
            }
        });
    }
    
    function createSkillItem(inputName, skills) {
        const skillItem = document.createElement('div');
        skillItem.className = 'skill-item mb-2 fade-in';
        skillItem.innerHTML = `
            <div class="input-group">
                <input type="text" class="form-control skill-input" 
                       name="${inputName}" placeholder="Enter a skill" autocomplete="off">
                <button type="button" class="btn btn-outline-danger remove-skill" title="Remove skill">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Setup autocomplete for new input
        const newInput = skillItem.querySelector('.skill-input');
        setupSkillAutocomplete(newInput, skills);
        
        return skillItem;
    }
    
    // Initialize skill management
    setupSkillManagement('#offered-skills', 'offered_skills', '#add-offered-skill');
    setupSkillManagement('#wanted-skills', 'wanted_skills', '#add-wanted-skill');
}

/**
 * Initialize rating system with performance optimizations
 */
function initializeRating() {
    // Use event delegation for better performance
    document.addEventListener('click', (e) => {
        if (e.target.matches('.star') || e.target.closest('.star')) {
            const star = e.target.closest('.star');
            const starRating = star.closest('.star-rating');
            const stars = starRating.querySelectorAll('.star');
            const hiddenInput = starRating.querySelector('input[type="hidden"]');
            
            const ratingValue = Array.from(stars).indexOf(star) + 1;
            if (hiddenInput) {
                hiddenInput.value = ratingValue;
            }
            updateStars(stars, ratingValue);
        }
    });
    
    document.addEventListener('mouseenter', (e) => {
        if (e.target.matches('.star') || e.target.closest('.star')) {
            const star = e.target.closest('.star');
            const starRating = star.closest('.star-rating');
            const stars = starRating.querySelectorAll('.star');
            
            const hoverValue = Array.from(stars).indexOf(star) + 1;
            updateStars(stars, hoverValue, true);
        }
    }, true);
    
    document.addEventListener('mouseleave', (e) => {
        if (e.target.matches('.star-rating') || e.target.closest('.star-rating')) {
            const starRating = e.target.closest('.star-rating');
            const stars = starRating.querySelectorAll('.star');
            const hiddenInput = starRating.querySelector('input[type="hidden"]');
            
            const currentValue = hiddenInput ? parseInt(hiddenInput.value) || 0 : 0;
            updateStars(stars, currentValue);
        }
    }, true);
}

function updateStars(stars, rating, isHover = false) {
    stars.forEach((star, index) => {
        const icon = star.querySelector('i');
        if (index < rating) {
            icon.className = 'fas fa-star';
            star.style.color = isHover ? '#ffca2c' : '#ffc107';
        } else {
            icon.className = 'far fa-star';
            star.style.color = '#dee2e6';
        }
    });
}

/**
 * Initialize notifications with performance optimizations
 */
function initializeNotifications() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    if (alerts.length === 0) return;
    
    // Batch DOM updates
    requestAnimationFrame(() => {
        alerts.forEach((alert, index) => {
            alert.classList.add('fade-in');
            
            // Stagger auto-hide timers
            setTimeout(() => {
                if (alert.parentNode) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, 5000 + (index * 100));
        });
    });
}

/**
 * Initialize lazy loading with Intersection Observer
 */
function initializeLazyLoading() {
    if (!('IntersectionObserver' in window)) {
        // Fallback for older browsers
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
        return;
    }
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            }
        });
    }, {
        rootMargin: '50px 0px',
        threshold: 0.01
    });
    
    const lazyImages = document.querySelectorAll('img.lazy');
    lazyImages.forEach(img => imageObserver.observe(img));
}

/**
 * Initialize virtual scrolling for large lists
 */
function initializeVirtualScrolling() {
    const virtualLists = document.querySelectorAll('.virtual-list');
    
    virtualLists.forEach(list => {
        const items = Array.from(list.children);
        if (items.length < 50) return; // Only virtualize large lists
        
        const itemHeight = 100; // Approximate item height
        const containerHeight = list.offsetHeight;
        const visibleItems = Math.ceil(containerHeight / itemHeight) + 5; // Buffer
        
        let scrollTop = 0;
        let startIndex = 0;
        let endIndex = Math.min(visibleItems, items.length);
        
        function updateVisibleItems() {
            const newStartIndex = Math.floor(scrollTop / itemHeight);
            const newEndIndex = Math.min(newStartIndex + visibleItems, items.length);
            
            if (newStartIndex !== startIndex || newEndIndex !== endIndex) {
                startIndex = newStartIndex;
                endIndex = newEndIndex;
                
                // Hide all items
                items.forEach(item => item.style.display = 'none');
                
                // Show visible items
                for (let i = startIndex; i < endIndex; i++) {
                    items[i].style.display = '';
                    items[i].style.transform = `translateY(${i * itemHeight}px)`;
                }
            }
        }
        
        list.addEventListener('scroll', debounce(() => {
            scrollTop = list.scrollTop;
            updateVisibleItems();
        }, 16), { passive: true }); // 60fps
        
        // Initial render
        updateVisibleItems();
    });
}

/**
 * Optimize images
 */
function optimizeImages() {
    const images = document.querySelectorAll('img:not([data-src])');
    
    images.forEach(img => {
        // Add loading attribute for native lazy loading
        if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
        }
        
        // Optimize image loading
        if (img.complete) {
            img.classList.add('loaded');
        } else {
            img.addEventListener('load', () => {
                img.classList.add('loaded');
            }, { once: true });
        }
    });
}

/**
 * Add animation to cards with performance optimization
 */
function animateCards() {
    const cards = document.querySelectorAll('.card');
    if (cards.length === 0) return;
    
    // Use Intersection Observer for better performance
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const card = entry.target;
                card.style.animationDelay = `${index * 0.1}s`;
                card.classList.add('fade-in');
                cardObserver.unobserve(card);
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => cardObserver.observe(card));
}

/**
 * Utility functions
 */

// Enhanced debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Optimized show loading state
function showLoading(element) {
    if (element && !element.dataset.loading) {
        const originalContent = element.innerHTML;
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        element.disabled = true;
        element.dataset.originalContent = originalContent;
        element.dataset.loading = 'true';
        return originalContent;
    }
}

// Optimized hide loading state
function hideLoading(element) {
    if (element && element.dataset.loading) {
        const originalContent = element.dataset.originalContent;
        if (originalContent) {
            element.innerHTML = originalContent;
            element.disabled = false;
            delete element.dataset.originalContent;
            delete element.dataset.loading;
        }
    }
}

// Smooth scroll with performance optimization
function smoothScrollTo(element) {
    if (element && 'scrollIntoView' in element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Optimized date formatting
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Optimized clipboard function
async function copyToClipboard(text) {
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
            showNotification('Copied to clipboard!', 'success');
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Copied to clipboard!', 'success');
        }
    } catch (err) {
        console.error('Failed to copy text: ', err);
        showNotification('Failed to copy text', 'error');
    }
}

// Optimized notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed notification-toast`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 400px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove with animation
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.add('fade-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 3000);
}

// Display search suggestions
function displaySearchSuggestions(suggestions) {
    // Implementation for search suggestions
    console.log('Search suggestions:', suggestions);
}

// Performance monitoring
function measurePerformance(name, fn) {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    console.log(`${name} took ${end - start} milliseconds`);
    return result;
}

// Export functions for global use
window.SkillSwapPlatform = {
    showLoading,
    hideLoading,
    smoothScrollTo,
    formatDate,
    isValidEmail,
    copyToClipboard,
    showNotification,
    debounce,
    throttle,
    measurePerformance,
    performanceCache,
    deduplicateRequest
};

// Add optimized CSS animations
const style = document.createElement('style');
style.textContent = `
    .fade-in {
        opacity: 0;
        animation: fadeIn 0.5s ease-in-out forwards;
    }
    
    .fade-out {
        animation: fadeOut 0.3s ease-in-out forwards;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-10px); }
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
    
    .loaded {
        animation: imageLoad 0.3s ease-in-out;
    }
    
    @keyframes imageLoad {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .spinner-border-sm {
        width: 1rem;
        height: 1rem;
    }
    
    .notification-toast {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .virtual-list {
        position: relative;
        overflow-y: auto;
    }
    
    .virtual-list .skill-item {
        position: absolute;
        width: 100%;
        transition: transform 0.1s ease;
    }
`;

document.head.appendChild(style);

// Main JavaScript for Skill Swap Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize skill management
    initializeSkillManagement();
    
    // Initialize rating system
    initializeRating();
    
    // Initialize notifications
    initializeNotifications();
    
    // Initialize lazy loading
    initializeLazyLoading();
    
    // Add fade-in animation to cards
    animateCards();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize form validation
 */
function initializeFormValidation() {
    // Real-time validation for registration form
    const registrationForm = document.querySelector('form[action*="register"]');
    if (registrationForm) {
        const passwordField = registrationForm.querySelector('#password');
        const confirmPasswordField = registrationForm.querySelector('#confirm_password');
        
        if (passwordField && confirmPasswordField) {
            function validatePasswordMatch() {
                const password = passwordField.value;
                const confirmPassword = confirmPasswordField.value;
                
                if (confirmPassword && password !== confirmPassword) {
                    confirmPasswordField.setCustomValidity('Passwords do not match');
                    confirmPasswordField.classList.add('is-invalid');
                } else {
                    confirmPasswordField.setCustomValidity('');
                    confirmPasswordField.classList.remove('is-invalid');
                }
            }
            
            passwordField.addEventListener('input', validatePasswordMatch);
            confirmPasswordField.addEventListener('input', validatePasswordMatch);
        }
    }
    
    // Add validation styling to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
        
        // Real-time validation for required fields
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchForm = document.querySelector('form[method="GET"]');
    const searchInput = document.querySelector('input[name="search"]');
    
    if (searchInput) {
        // Add search suggestions/autocomplete
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    // Could implement real-time search suggestions here
                    console.log('Searching for:', query);
                }, 300);
            }
        });
        
        // Enhance search with Enter key
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (searchForm) {
                    searchForm.submit();
                }
            }
        });
    }
    
    // Clear search functionality
    const clearSearchBtn = document.querySelector('.clear-search');
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (searchInput) {
                searchInput.value = '';
            }
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
 * Initialize skill management functionality
 */
function initializeSkillManagement() {
    // Skill autocomplete functionality
    function setupSkillAutocomplete(input, skills) {
        if (!input || !skills) return;
        
        input.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            const suggestions = skills.filter(skill => 
                skill.toLowerCase().includes(value)
            ).slice(0, 5);
            
            // Remove existing datalist
            const existingDatalist = document.querySelector(`#${this.getAttribute('list')}`);
            if (existingDatalist) {
                existingDatalist.remove();
            }
            
            // Create new datalist
            if (suggestions.length > 0 && value.length >= 2) {
                const datalist = document.createElement('datalist');
                const listId = 'skills-list-' + Math.random().toString(36).substr(2, 9);
                datalist.id = listId;
                
                suggestions.forEach(skill => {
                    const option = document.createElement('option');
                    option.value = skill;
                    datalist.appendChild(option);
                });
                
                this.setAttribute('list', listId);
                this.parentNode.appendChild(datalist);
            }
        });
    }
    
    // Initialize autocomplete for existing skill inputs
    const skillInputs = document.querySelectorAll('.skill-input');
    const allSkills = window.allSkills || []; // Assume this is set from template
    
    skillInputs.forEach(input => {
        setupSkillAutocomplete(input, allSkills);
    });
    
    // Dynamic skill addition/removal
    function setupSkillManagement(containerId, inputName, buttonId) {
        const container = document.querySelector(containerId);
        const addButton = document.querySelector(buttonId);
        
        if (!container || !addButton) return;
        
        addButton.addEventListener('click', function() {
            const skillItem = document.createElement('div');
            skillItem.className = 'skill-item mb-2 fade-in';
            skillItem.innerHTML = `
                <div class="input-group">
                    <input type="text" class="form-control skill-input" 
                           name="${inputName}" placeholder="Enter a skill">
                    <button type="button" class="btn btn-outline-danger remove-skill" title="Remove skill">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            container.appendChild(skillItem);
            
            // Setup autocomplete for new input
            const newInput = skillItem.querySelector('.skill-input');
            setupSkillAutocomplete(newInput, allSkills);
            
            // Focus on new input
            newInput.focus();
            
            // Setup remove functionality
            const removeBtn = skillItem.querySelector('.remove-skill');
            removeBtn.addEventListener('click', function() {
                skillItem.style.animation = 'fadeOut 0.3s ease-out';
                setTimeout(() => {
                    skillItem.remove();
                }, 300);
            });
        });
        
        // Setup remove functionality for existing items
        container.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-skill') || 
                e.target.parentNode.classList.contains('remove-skill')) {
                e.preventDefault();
                
                const skillItem = e.target.closest('.skill-item');
                const skillItems = container.querySelectorAll('.skill-item');
                
                if (skillItems.length > 1) {
                    skillItem.style.animation = 'fadeOut 0.3s ease-out';
                    setTimeout(() => {
                        skillItem.remove();
                    }, 300);
                } else {
                    // Clear the input instead of removing the last item
                    const input = skillItem.querySelector('input');
                    if (input) {
                        input.value = '';
                        input.focus();
                    }
                }
            }
        });
    }
    
    // Initialize skill management for different sections
    setupSkillManagement('#offered-skills', 'offered_skills', '#add-offered-skill');
    setupSkillManagement('#wanted-skills', 'wanted_skills', '#add-wanted-skill');
}

/**
 * Initialize rating system
 */
function initializeRating() {
    const ratingInputs = document.querySelectorAll('input[name="rating"]');
    
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            const ratingValue = parseInt(this.value);
            const starContainer = this.closest('form').querySelector('.rating-stars');
            
            if (starContainer) {
                updateStarDisplay(starContainer, ratingValue);
            }
        });
    });
    
    // Interactive star rating
    const starRatings = document.querySelectorAll('.star-rating');
    starRatings.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        const hiddenInput = rating.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const ratingValue = index + 1;
                if (hiddenInput) {
                    hiddenInput.value = ratingValue;
                }
                updateStars(stars, ratingValue);
            });
            
            star.addEventListener('mouseenter', function() {
                const hoverValue = index + 1;
                updateStars(stars, hoverValue, true);
            });
        });
        
        rating.addEventListener('mouseleave', function() {
            const currentValue = hiddenInput ? parseInt(hiddenInput.value) || 0 : 0;
            updateStars(stars, currentValue);
        });
    });
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
 * Initialize notifications
 */
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add smooth animation to alerts
    alerts.forEach(alert => {
        alert.classList.add('fade-in');
    });
}

/**
 * Initialize lazy loading for images
 */
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img.lazy');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

/**
 * Add animation to cards
 */
function animateCards() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
}

/**
 * Utility functions
 */

// Debounce function for search
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

// Show loading state
function showLoading(element) {
    if (element) {
        const originalContent = element.innerHTML;
        element.innerHTML = '<span class="loading"></span> Loading...';
        element.disabled = true;
        return originalContent;
    }
}

// Hide loading state
function hideLoading(element, originalContent) {
    if (element && originalContent) {
        element.innerHTML = originalContent;
        element.disabled = false;
    }
}

// Smooth scroll to element
function smoothScrollTo(element) {
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Format date for display
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Copy text to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copied to clipboard!', 'success');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(notification);
        bsAlert.close();
    }, 3000);
}

// Enhanced form submission with loading state
function enhanceFormSubmission() {
    const forms = document.querySelectorAll('form[data-enhance="true"]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalContent = showLoading(submitBtn);
                
                // Store original content to restore if needed
                submitBtn.setAttribute('data-original-content', originalContent);
            }
        });
    });
}

// Initialize enhanced form submission
document.addEventListener('DOMContentLoaded', enhanceFormSubmission);

// Add CSS animation classes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(style);

// Export functions for global use
window.SkillSwapPlatform = {
    showLoading,
    hideLoading,
    smoothScrollTo,
    formatDate,
    isValidEmail,
    copyToClipboard,
    showNotification,
    debounce
};

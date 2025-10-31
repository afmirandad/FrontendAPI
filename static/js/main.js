/**
 * Main JavaScript file for UI interactions and utilities
 */

document.addEventListener('DOMContentLoaded', () => {
    // Flash message auto-dismiss
    initFlashMessages();
    
    // Form validation
    initFormValidation();
    
    // Smooth animations
    initAnimations();
});

/**
 * Initialize flash message functionality
 */
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(flash => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            dismissFlash(flash);
        }, 5000);
        
        // Click to dismiss
        const closeBtn = flash.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissFlash(flash);
            });
        }
    });
}

/**
 * Dismiss a flash message with animation
 */
function dismissFlash(flash) {
    flash.style.animation = 'slideOut 0.3s ease-out forwards';
    setTimeout(() => {
        flash.remove();
    }, 300);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
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
`;
document.head.appendChild(style);

/**
 * Initialize form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', () => {
                validateInput(input);
            });
            
            input.addEventListener('input', () => {
                if (input.classList.contains('error')) {
                    validateInput(input);
                }
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', (e) => {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Por favor completa todos los campos correctamente', 'error');
            }
        });
    });
}

/**
 * Validate a single input field
 */
function validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    let isValid = true;
    let errorMessage = '';
    
    // Check if empty
    if (!value) {
        isValid = false;
        errorMessage = 'Este campo es requerido';
    }
    // Email validation
    else if (type === 'email' && !isValidEmail(value)) {
        isValid = false;
        errorMessage = 'Por favor ingresa un email válido';
    }
    // Password validation
    else if (type === 'password' && value.length < 6) {
        isValid = false;
        errorMessage = 'La contraseña debe tener al menos 6 caracteres';
    }
    
    // Update UI
    if (isValid) {
        input.classList.remove('error');
        removeErrorMessage(input);
    } else {
        input.classList.add('error');
        showErrorMessage(input, errorMessage);
    }
    
    return isValid;
}

/**
 * Check if email is valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Show error message below input
 */
function showErrorMessage(input, message) {
    removeErrorMessage(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'input-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: var(--error-color);
        font-size: 0.875rem;
        margin-top: 0.25rem;
        animation: fadeIn 0.2s ease-out;
    `;
    
    input.parentNode.appendChild(errorDiv);
}

/**
 * Remove error message
 */
function removeErrorMessage(input) {
    const existingError = input.parentNode.querySelector('.input-error');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Show notification (similar to flash message)
 */
function showNotification(message, type = 'info') {
    const container = document.querySelector('.flash-container') || createFlashContainer();
    
    const flash = document.createElement('div');
    flash.className = `flash flash-${type}`;
    flash.innerHTML = `
        ${message}
        <span class="flash-close">&times;</span>
    `;
    
    container.appendChild(flash);
    
    // Auto-dismiss
    setTimeout(() => {
        dismissFlash(flash);
    }, 5000);
    
    // Click to dismiss
    const closeBtn = flash.querySelector('.flash-close');
    closeBtn.addEventListener('click', () => {
        dismissFlash(flash);
    });
}

/**
 * Create flash container if it doesn't exist
 */
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-container';
    document.body.appendChild(container);
    return container;
}

/**
 * Initialize animations
 */
function initAnimations() {
    // Add fade-in class to elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe all cards
    document.querySelectorAll('.user-card, .auth-card').forEach(card => {
        observer.observe(card);
    });
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility: Throttle function
 */
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

// Export utilities for use in other scripts
window.utils = {
    debounce,
    throttle,
    showNotification
};

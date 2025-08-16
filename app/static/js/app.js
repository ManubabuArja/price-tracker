// Price Tracker Application JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // URL validation for product tracking
    const urlInput = document.querySelector('input[name="url"]');
    if (urlInput) {
        urlInput.addEventListener('blur', function() {
            const url = this.value.trim();
            if (url && !isValidEcommerceUrl(url)) {
                this.classList.add('is-invalid');
                if (!this.nextElementSibling || !this.nextElementSibling.classList.contains('invalid-feedback')) {
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = 'Please enter a valid URL from supported platforms (Amazon, Flipkart, Myntra, Meesho)';
                    this.parentNode.appendChild(feedback);
                }
            } else {
                this.classList.remove('is-invalid');
                const feedback = this.parentNode.querySelector('.invalid-feedback');
                if (feedback) {
                    feedback.remove();
                }
            }
        });
    }

    // Price input formatting
    const priceInputs = document.querySelectorAll('input[name="target"], input[step="0.01"]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value.replace(/[^\d.]/g, '');
            if (value.split('.').length > 2) {
                value = value.replace(/\.+$/, '');
            }
            this.value = value;
        });
    });

    // Table row hover effects
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Copy URL to clipboard functionality
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url) {
                navigator.clipboard.writeText(url).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    this.classList.add('btn-success');
                    this.classList.remove('btn-outline-secondary');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-secondary');
                    }, 2000);
                });
            }
        });
    });

    // Price change indicators
    const priceElements = document.querySelectorAll('.price-tag');
    priceElements.forEach(priceEl => {
        const price = parseFloat(priceEl.textContent.replace('₹', ''));
        if (price > 10000) {
            priceEl.classList.add('text-danger');
        } else if (price > 5000) {
            priceEl.classList.add('text-warning');
        } else {
            priceEl.classList.add('text-success');
        }
    });

    // Auto-refresh functionality for price updates
    if (window.location.pathname.includes('/history')) {
        setInterval(() => {
            // Refresh the page every 5 minutes to get updated prices
            // This is a simple approach - in production, you'd use AJAX
        }, 300000);
    }
});

// Helper function to validate e-commerce URLs
function isValidEcommerceUrl(url) {
    const supportedPlatforms = [
        'amazon.in', 'amazon.com',
        'flipkart.com',
        'myntra.com',
        'meesho.com'
    ];
    
    try {
        const urlObj = new URL(url);
        return supportedPlatforms.some(platform => 
            urlObj.hostname.includes(platform)
        );
    } catch (e) {
        return false;
    }
}

// Add loading state to buttons
function setLoadingState(button, isLoading) {
    if (isLoading) {
        button.innerHTML = '<span class="loading"></span> Loading...';
        button.disabled = true;
    } else {
        button.innerHTML = button.getAttribute('data-original-text') || 'Submit';
        button.disabled = false;
    }
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type} show`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        max-width: 300px;
        border-left: 4px solid var(--${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'}-color);
    `;
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Export functionality for price data
function exportToCSV(data, filename) {
    const csvContent = "data:text/csv;charset=utf-8," + data;
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

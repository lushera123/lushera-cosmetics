/* ═══════════════════════════════════════════════════════════════
   MODERN COSMETICS ECOMMERCE - MAIN JAVASCRIPT
   ═══════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════
  // MOBILE MENU TOGGLE
  // ═══════════════════════════════════════════════════════════════
  const mobileToggle = document.querySelector('.mobile-toggle');
  const navMenu = document.querySelector('.nav-menu');
  const body = document.body;

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
        navMenu.classList.remove('active');
        body.style.overflow = '';
      }
    });

    // Close menu on link click
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        body.style.overflow = '';
      });
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // HEADER SCROLL EFFECT
  // ═══════════════════════════════════════════════════════════════
  const header = document.querySelector('.header');
  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
  });

  // ═══════════════════════════════════════════════════════════════
  // SEARCH TOGGLE
  // ═══════════════════════════════════════════════════════════════
  const searchToggle = document.querySelector('.search-toggle');
  const searchPopup = document.querySelector('.search-popup');
  const searchClose = document.querySelector('.search-close');

  if (searchToggle && searchPopup) {
    searchToggle.addEventListener('click', (e) => {
      e.preventDefault();
      searchPopup.classList.add('active');
      document.querySelector('.search-popup input')?.focus();
    });

    if (searchClose) {
      searchClose.addEventListener('click', () => {
        searchPopup.classList.remove('active');
      });
    }

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && searchPopup.classList.contains('active')) {
        searchPopup.classList.remove('active');
      }
    });

    // Close on backdrop click
    searchPopup.addEventListener('click', (e) => {
      if (e.target === searchPopup) {
        searchPopup.classList.remove('active');
      }
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // QUANTITY CONTROLS
  // ═══════════════════════════════════════════════════════════════
  document.querySelectorAll('.quantity-control').forEach(control => {
    const minusBtn = control.querySelector('.qty-minus');
    const plusBtn = control.querySelector('.qty-plus');
    const input = control.querySelector('.qty-input');

    if (minusBtn && plusBtn && input) {
      minusBtn.addEventListener('click', () => {
        const currentValue = parseInt(input.value) || 1;
        if (currentValue > 1) {
          input.value = currentValue - 1;
          input.dispatchEvent(new Event('change'));
        }
      });

      plusBtn.addEventListener('click', () => {
        const currentValue = parseInt(input.value) || 1;
        const max = parseInt(input.getAttribute('max')) || 999;
        if (currentValue < max) {
          input.value = currentValue + 1;
          input.dispatchEvent(new Event('change'));
        }
      });

      input.addEventListener('input', () => {
        const value = parseInt(input.value) || 1;
        const min = parseInt(input.getAttribute('min')) || 1;
        const max = parseInt(input.getAttribute('max')) || 999;
        
        if (value < min) input.value = min;
        if (value > max) input.value = max;
      });
    }
  });

  // ═══════════════════════════════════════════════════════════════
  // WISHLIST TOGGLE
  // ═══════════════════════════════════════════════════════════════
  document.querySelectorAll('.wishlist-toggle').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      this.classList.toggle('active');
      
      // Add animation
      this.style.transform = 'scale(1.3)';
      setTimeout(() => {
        this.style.transform = '';
      }, 200);
    });
  });

  // ═══════════════════════════════════════════════════════════════
  // PRODUCT IMAGE GALLERY
  // ═══════════════════════════════════════════════════════════════
  const thumbnails = document.querySelectorAll('.product-thumbnail');
  const mainImage = document.querySelector('.product-main-image');

  thumbnails.forEach(thumb => {
    thumb.addEventListener('click', function() {
      thumbnails.forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      
      if (mainImage) {
        const newSrc = this.getAttribute('data-image');
        mainImage.src = newSrc;
      }
    });
  });

  // ═══════════════════════════════════════════════════════════════
  // VARIANT SELECTOR
  // ═══════════════════════════════════════════════════════════════
  const variantButtons = document.querySelectorAll('.variant-btn');
  const variantInput = document.getElementById('selected-variant-id');
  const stockStatus = document.getElementById('stock-status');
  const addToCartBtn = document.getElementById('add-to-cart-btn');

  variantButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      // Remove active class from all buttons
      variantButtons.forEach(b => b.classList.remove('active'));
      
      // Add active class to clicked button
      this.classList.add('active');
      
      // Update hidden input
      if (variantInput) {
        variantInput.value = this.getAttribute('data-variant-id');
      }
      
      // Update stock status
      const stock = parseInt(this.getAttribute('data-stock'));
      if (stockStatus) {
        if (stock > 0) {
          stockStatus.innerHTML = `<span class="text-success">✓ In Stock — ${stock} available</span>`;
          if (addToCartBtn) addToCartBtn.disabled = false;
        } else {
          stockStatus.innerHTML = '<span class="text-danger">✗ Out of Stock</span>';
          if (addToCartBtn) addToCartBtn.disabled = true;
        }
      }
    });
  });

  // ═══════════════════════════════════════════════════════════════
  // FILTER TOGGLE (MOBILE)
  // ═══════════════════════════════════════════════════════════════
  const filterToggle = document.querySelector('.filter-toggle');
  const filterSidebar = document.querySelector('.filter-sidebar');
  const filterClose = document.querySelector('.filter-close');

  if (filterToggle && filterSidebar) {
    filterToggle.addEventListener('click', () => {
      filterSidebar.classList.add('active');
      body.style.overflow = 'hidden';
    });

    if (filterClose) {
      filterClose.addEventListener('click', () => {
        filterSidebar.classList.remove('active');
        body.style.overflow = '';
      });
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // SMOOTH SCROLL
  // ═══════════════════════════════════════════════════════════════
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href !== '#0') {
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });

  // ═══════════════════════════════════════════════════════════════
  // LAZY LOADING IMAGES
  // ═══════════════════════════════════════════════════════════════
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          const src = img.getAttribute('data-src');
          if (src) {
            img.src = src;
            img.removeAttribute('data-src');
            img.classList.add('loaded');
          }
          observer.unobserve(img);
        }
      });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // TOAST NOTIFICATIONS
  // ═══════════════════════════════════════════════════════════════
  window.showToast = function(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <div class="toast-content">
        <span class="toast-icon">${getToastIcon(type)}</span>
        <span class="toast-message">${message}</span>
      </div>
      <button class="toast-close">&times;</button>
    `;

    const container = document.querySelector('.toast-container') || createToastContainer();
    container.appendChild(toast);

    // Animate in
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto dismiss
    const timeout = setTimeout(() => dismissToast(toast), 5000);

    // Manual dismiss
    toast.querySelector('.toast-close').addEventListener('click', () => {
      clearTimeout(timeout);
      dismissToast(toast);
    });
  };

  function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
  }

  function dismissToast(toast) {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }

  function getToastIcon(type) {
    const icons = {
      success: '✓',
      error: '✕',
      warning: '⚠',
      info: 'ℹ'
    };
    return icons[type] || icons.info;
  }

  // ═══════════════════════════════════════════════════════════════
  // DJANGO MESSAGES TO TOASTS
  // ═══════════════════════════════════════════════════════════════
  const djangoMessages = document.getElementById('django-messages');
  if (djangoMessages) {
    djangoMessages.querySelectorAll('span[data-tag]').forEach((msg, index) => {
      setTimeout(() => {
        const tag = msg.getAttribute('data-tag');
        const type = tag === 'error' ? 'error' : tag === 'success' ? 'success' : 'info';
        showToast(msg.textContent.trim(), type);
      }, index * 150);
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // FORM VALIDATION
  // ═══════════════════════════════════════════════════════════════
  document.querySelectorAll('form[data-validate]').forEach(form => {
    form.addEventListener('submit', function(e) {
      let isValid = true;
      
      this.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add('error');
          
          // Show error message
          let errorMsg = field.nextElementSibling;
          if (!errorMsg || !errorMsg.classList.contains('error-message')) {
            errorMsg = document.createElement('span');
            errorMsg.className = 'error-message';
            errorMsg.textContent = 'This field is required';
            field.parentNode.insertBefore(errorMsg, field.nextSibling);
          }
        } else {
          field.classList.remove('error');
          const errorMsg = field.nextElementSibling;
          if (errorMsg && errorMsg.classList.contains('error-message')) {
            errorMsg.remove();
          }
        }
      });

      if (!isValid) {
        e.preventDefault();
        showToast('Please fill in all required fields', 'error');
      }
    });
  });

  // ═══════════════════════════════════════════════════════════════
  // PRICE RANGE SLIDER
  // ═══════════════════════════════════════════════════════════════
  const priceMin = document.getElementById('price-min');
  const priceMax = document.getElementById('price-max');
  const priceMinValue = document.getElementById('price-min-value');
  const priceMaxValue = document.getElementById('price-max-value');

  if (priceMin && priceMax) {
    priceMin.addEventListener('input', function() {
      if (priceMinValue) priceMinValue.textContent = this.value;
      if (parseInt(this.value) > parseInt(priceMax.value)) {
        this.value = priceMax.value;
      }
    });

    priceMax.addEventListener('input', function() {
      if (priceMaxValue) priceMaxValue.textContent = this.value;
      if (parseInt(this.value) < parseInt(priceMin.value)) {
        this.value = priceMin.value;
      }
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // NEWSLETTER FORM
  // ═══════════════════════════════════════════════════════════════
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const email = this.querySelector('input[type="email"]').value;
      
      // Simulate API call
      setTimeout(() => {
        showToast('Thank you for subscribing!', 'success');
        this.reset();
      }, 500);
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // INITIALIZE ON DOM READY
  // ═══════════════════════════════════════════════════════════════
  console.log('🎨 Modern Cosmetics Store - Initialized');

})();

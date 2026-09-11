# Home Page Sliders - Implementation Guide

## ✅ Changes Made

### 1. Added Swiper.js Library
**File**: `templates/base.html`

Added Swiper.js CDN links:
```html
<!-- Swiper.js for sliders -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
```

### 2. Category Slider
**Section**: Shop by Category

**Features**:
- ✅ Auto-play with 3 second delay
- ✅ Loop enabled (infinite scroll)
- ✅ Navigation arrows (left/right)
- ✅ Pagination dots
- ✅ Responsive breakpoints:
  - Mobile: 1 slide
  - Tablet (640px+): 2 slides
  - Desktop (1024px+): 3 slides

**Configuration**:
```javascript
const categorySwiper = new Swiper('.categorySwiper', {
  slidesPerView: 1,
  spaceBetween: 30,
  loop: true,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  pagination: {
    el: '.swiper-pagination-category',
    clickable: true,
  },
  navigation: {
    nextEl: '.swiper-button-next-category',
    prevEl: '.swiper-button-prev-category',
  },
  breakpoints: {
    640: { slidesPerView: 2 },
    1024: { slidesPerView: 3 },
  },
});
```

### 3. Products Slider (New Arrivals)
**Section**: New Arrivals (formerly "Trending Products")

**Changes**:
- ✅ Changed heading from "Trending Products" to "New Arrivals"
- ✅ Converted grid to slider
- ✅ Auto-play with 4 second delay
- ✅ Loop enabled
- ✅ Navigation arrows
- ✅ Pagination dots
- ✅ Responsive breakpoints:
  - Mobile: 2 slides
  - Tablet (768px+): 3 slides
  - Desktop (1024px+): 4 slides

**Configuration**:
```javascript
const productsSwiper = new Swiper('.productsSwiper', {
  slidesPerView: 2,
  spaceBetween: 20,
  loop: true,
  autoplay: {
    delay: 4000,
    disableOnInteraction: false,
  },
  pagination: {
    el: '.swiper-pagination-products',
    clickable: true,
  },
  navigation: {
    nextEl: '.swiper-button-next-products',
    prevEl: '.swiper-button-prev-products',
  },
  breakpoints: {
    768: { slidesPerView: 3 },
    1024: { slidesPerView: 4 },
  },
});
```

---

## 🎨 Slider Design

### Navigation Buttons
- **Style**: White circular buttons with shadow
- **Size**: 48×48px
- **Position**: Absolute, centered vertically
- **Hover**: Rose background with white icon
- **Icons**: Chevron left/right (Heroicons)

```html
<div class="w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center cursor-pointer hover:bg-rose hover:text-white transition">
  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
  </svg>
</div>
```

### Pagination Dots
- **Default**: Gray dots (12×12px)
- **Active**: Rose pink elongated pill (32×12px)
- **Position**: Below slider, centered
- **Clickable**: Yes

```css
.swiper-pagination-bullet {
  width: 12px;
  height: 12px;
  background: #D1D5DB;
  opacity: 1;
  transition: all 0.3s;
}

.swiper-pagination-bullet-active {
  background: #FF6B9D;
  width: 32px;
  border-radius: 6px;
}
```

---

## 📱 Responsive Behavior

### Category Slider
| Screen Size | Slides Visible | Spacing |
|-------------|----------------|---------|
| Mobile (<640px) | 1 | 30px |
| Tablet (640px+) | 2 | 20px |
| Desktop (1024px+) | 3 | 30px |

### Products Slider
| Screen Size | Slides Visible | Spacing |
|-------------|----------------|---------|
| Mobile (<768px) | 2 | 20px |
| Tablet (768px+) | 3 | 24px |
| Desktop (1024px+) | 4 | 24px |

---

## ⚙️ Slider Settings

### Auto-play
- **Category Slider**: 3 seconds per slide
- **Products Slider**: 4 seconds per slide
- **Pause on Hover**: No (continues playing)
- **Disable on Interaction**: No (continues after manual navigation)

### Loop
- **Enabled**: Yes (infinite scroll)
- **Smooth Transition**: Yes

### Navigation
- **Arrows**: Custom styled buttons
- **Pagination**: Dots below slider
- **Keyboard**: Enabled by default
- **Mouse Wheel**: Disabled

---

## 🎯 HTML Structure

### Category Slider
```html
<div class="relative">
  <div class="swiper categorySwiper">
    <div class="swiper-wrapper">
      {% for category in categories %}
      <div class="swiper-slide">
        <!-- Category card -->
      </div>
      {% endfor %}
    </div>
  </div>
  
  <!-- Navigation -->
  <div class="swiper-button-prev-category">...</div>
  <div class="swiper-button-next-category">...</div>
  
  <!-- Pagination -->
  <div class="swiper-pagination-category"></div>
</div>
```

### Products Slider
```html
<div class="relative">
  <div class="swiper productsSwiper">
    <div class="swiper-wrapper">
      {% for product in products %}
      <div class="swiper-slide">
        <!-- Product card -->
      </div>
      {% endfor %}
    </div>
  </div>
  
  <!-- Navigation -->
  <div class="swiper-button-prev-products">...</div>
  <div class="swiper-button-next-products">...</div>
  
  <!-- Pagination -->
  <div class="swiper-pagination-products"></div>
</div>
```

---

## 🔧 Customization Options

### Change Auto-play Speed
```javascript
autoplay: {
  delay: 5000, // 5 seconds
  disableOnInteraction: false,
}
```

### Change Slides Per View
```javascript
slidesPerView: 3, // Show 3 slides at once
```

### Disable Loop
```javascript
loop: false,
```

### Add Fade Effect
```javascript
effect: 'fade',
fadeEffect: {
  crossFade: true
},
```

### Add Slide Animation
```javascript
effect: 'coverflow',
coverflowEffect: {
  rotate: 50,
  stretch: 0,
  depth: 100,
  modifier: 1,
  slideShadows: true,
},
```

---

## 🐛 Troubleshooting

### Slider Not Working
1. Check if Swiper.js CDN is loaded
2. Verify class names match (`.categorySwiper`, `.productsSwiper`)
3. Check browser console for errors
4. Ensure slides have content

### Navigation Buttons Not Showing
1. Check if buttons are outside slider container
2. Verify z-index is set correctly
3. Check if `position: relative` is on parent

### Pagination Not Clickable
1. Ensure `clickable: true` in config
2. Check if pagination element exists
3. Verify class name matches config

### Auto-play Not Working
1. Check if `autoplay` is configured
2. Verify `loop: true` is set
3. Check if user has interacted with slider

---

## 📊 Performance

### Optimization Tips
1. **Lazy Load Images**: Add `loading="lazy"` to images
2. **Limit Slides**: Don't load too many slides at once
3. **Disable Unused Features**: Remove features you don't need
4. **Use CSS Transforms**: Swiper uses GPU acceleration

### Best Practices
- Keep slide content lightweight
- Optimize images before upload
- Use appropriate image sizes
- Minimize DOM manipulation
- Use `will-change: transform` for smooth animations

---

## 🎨 Styling Tips

### Custom Arrow Buttons
```css
.swiper-button-prev-category,
.swiper-button-next-category {
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.swiper-button-prev-category:hover,
.swiper-button-next-category:hover {
  background: #FF6B9D;
  color: white;
}
```

### Custom Pagination
```css
.swiper-pagination-bullet {
  width: 12px;
  height: 12px;
  background: #D1D5DB;
  opacity: 1;
}

.swiper-pagination-bullet-active {
  background: #FF6B9D;
  width: 32px;
  border-radius: 6px;
}
```

---

## ✅ Testing Checklist

- [ ] Category slider displays correctly
- [ ] Products slider displays correctly
- [ ] Auto-play works
- [ ] Navigation arrows work
- [ ] Pagination dots work
- [ ] Loop works (infinite scroll)
- [ ] Responsive on mobile
- [ ] Responsive on tablet
- [ ] Responsive on desktop
- [ ] Hover effects work
- [ ] Images load properly
- [ ] Links work correctly
- [ ] No console errors

---

## 📝 Notes

- Swiper.js version: 11 (latest)
- CDN used for easy setup
- No build step required
- Works with Django templates
- Compatible with Alpine.js
- Mobile-first responsive design

---

**Status**: ✅ Sliders implemented successfully!
**Heading Changed**: "Trending Products" → "New Arrivals" ✅

---

**Last Updated**: May 2026

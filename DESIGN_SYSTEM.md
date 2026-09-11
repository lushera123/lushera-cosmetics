# BeautyBloom Design System

## 🎨 Color Palette

### Primary Colors
```css
Rose Pink:     #FF6B9D  (Primary CTA, Links, Accents)
Rose Dark:     #E5527D  (Hover states)
Cream:         #FFF8F3  (Light backgrounds)
Beige:         #F5F0EB  (Card backgrounds)
Charcoal:      #1A1A1A  (Dark text, buttons)
Gold:          #D4AF37  (Accent, badges)
```

### Semantic Colors
```css
Success:       #10B981  (Green - Delivered, Success messages)
Warning:       #F59E0B  (Yellow - Pending, Warnings)
Error:         #EF4444  (Red - Cancelled, Errors)
Info:          #3B82F6  (Blue - Shipped, Info messages)
```

---

## 📝 Typography

### Font Families
```css
Headings:      'Playfair Display', serif
Body:          'Poppins', sans-serif
```

### Font Sizes
```css
Hero Title:    text-5xl (48px)
Page Title:    text-4xl (36px)
Section Title: text-3xl (30px)
Card Title:    text-2xl (24px)
Heading:       text-xl (20px)
Body Large:    text-lg (18px)
Body:          text-base (16px)
Body Small:    text-sm (14px)
Caption:       text-xs (12px)
```

### Font Weights
```css
Light:         font-light (300)
Regular:       font-normal (400)
Medium:        font-medium (500)
Semibold:      font-semibold (600)
Bold:          font-bold (700)
```

---

## 🔲 Spacing System

### Padding/Margin Scale
```css
xs:   p-2  (8px)
sm:   p-3  (12px)
md:   p-4  (16px)
lg:   p-6  (24px)
xl:   p-8  (32px)
2xl:  p-12 (48px)
3xl:  p-16 (64px)
```

### Common Patterns
```css
Card Padding:        p-6 md:p-8
Section Padding:     py-12 md:py-16
Container Padding:   px-4 sm:px-6 lg:px-8
Button Padding:      px-6 py-3 (medium)
                     px-8 py-4 (large)
```

---

## 🎯 Border Radius

### Radius Scale
```css
Small:    rounded-lg    (8px)  - Small cards, inputs
Medium:   rounded-xl    (12px) - Images, cards
Large:    rounded-2xl   (16px) - Large cards, sections
Full:     rounded-full  (9999px) - Buttons, badges, avatars
```

### Usage
```css
Buttons:         rounded-full
Cards:           rounded-2xl
Images:          rounded-xl
Input Fields:    rounded-xl
Badges:          rounded-full
Avatars:         rounded-full
```

---

## 🖼️ Components

### Buttons

#### Primary Button
```html
<button class="bg-rose text-white px-8 py-4 rounded-full font-semibold hover:bg-rose-dark transition shadow-lg hover:shadow-xl">
  Button Text
</button>
```

#### Secondary Button
```html
<button class="bg-white border-2 border-charcoal text-charcoal px-8 py-4 rounded-full font-semibold hover:bg-charcoal hover:text-white transition">
  Button Text
</button>
```

#### Outline Button
```html
<button class="border-2 border-rose text-rose px-6 py-3 rounded-full font-semibold hover:bg-rose hover:text-white transition">
  Button Text
</button>
```

### Cards

#### Product Card
```html
<div class="group bg-white rounded-2xl overflow-hidden border border-gray-100 hover:shadow-xl transition-all duration-300">
  <div class="relative overflow-hidden aspect-[3/4]">
    <img src="..." class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
  </div>
  <div class="p-4">
    <!-- Content -->
  </div>
</div>
```

#### Info Card
```html
<div class="bg-cream rounded-2xl p-8">
  <h3 class="text-2xl font-serif font-bold mb-6">Title</h3>
  <!-- Content -->
</div>
```

### Forms

#### Input Field
```html
<input type="text" class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-rose focus:outline-none transition" placeholder="Enter text">
```

#### Textarea
```html
<textarea rows="3" class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-rose focus:outline-none transition" placeholder="Enter text"></textarea>
```

#### Checkbox
```html
<input type="checkbox" class="w-4 h-4 text-rose border-gray-300 rounded focus:ring-rose">
```

#### Radio Button
```html
<input type="radio" class="w-5 h-5 text-rose focus:ring-rose">
```

### Badges

#### Status Badge
```html
<!-- Success -->
<span class="px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700">
  Delivered
</span>

<!-- Warning -->
<span class="px-3 py-1 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-700">
  Pending
</span>

<!-- Error -->
<span class="px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700">
  Cancelled
</span>

<!-- Info -->
<span class="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
  Shipped
</span>
```

#### Tag Badge
```html
<span class="bg-rose text-white text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wide">
  New Arrival
</span>
```

---

## 🎭 Hover Effects

### Scale on Hover
```css
hover:scale-105 transition-transform duration-300
```

### Shadow on Hover
```css
hover:shadow-xl transition-shadow duration-300
```

### Color Change on Hover
```css
hover:text-rose transition-colors duration-200
hover:bg-rose-dark transition-colors duration-200
```

### Image Zoom on Hover
```css
group-hover:scale-110 transition-transform duration-500
```

---

## 📱 Responsive Grid

### Product Grid
```html
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
  <!-- Products -->
</div>
```

### Two Column Layout
```html
<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
  <!-- Content -->
</div>
```

### Three Column Layout
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
  <!-- Content -->
</div>
```

### Sidebar Layout
```html
<div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
  <div class="lg:col-span-1"><!-- Sidebar --></div>
  <div class="lg:col-span-3"><!-- Main Content --></div>
</div>
```

---

## 🎬 Animations

### Fade In
```html
<div x-show="open" x-transition class="...">
  <!-- Content -->
</div>
```

### Slide In from Right
```html
<div x-show="open" 
     x-transition:enter="transform transition ease-out duration-300"
     x-transition:enter-start="translate-x-full"
     x-transition:enter-end="translate-x-0"
     x-transition:leave="transform transition ease-in duration-200"
     x-transition:leave-start="translate-x-0"
     x-transition:leave-end="translate-x-full">
  <!-- Content -->
</div>
```

### Pulse Animation
```html
<div class="animate-pulse">
  <!-- Content -->
</div>
```

---

## 🔍 Icons

### Icon Library
Using Heroicons (outline style) via inline SVG

### Common Icons
```html
<!-- Search -->
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
</svg>

<!-- Heart (Wishlist) -->
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
</svg>

<!-- Shopping Cart -->
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"/>
</svg>

<!-- User -->
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
</svg>

<!-- Check (Success) -->
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
</svg>

<!-- X (Close) -->
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
</svg>
```

---

## 📐 Layout Patterns

### Container
```html
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Content -->
</div>
```

### Section
```html
<section class="py-12 md:py-16 bg-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Content -->
  </div>
</section>
```

### Sticky Sidebar
```html
<div class="sticky top-24">
  <!-- Sidebar content -->
</div>
```

---

## 🎨 Gradient Backgrounds

### Rose Gradient
```css
bg-gradient-to-br from-rose to-rose-dark
```

### Purple Gradient
```css
bg-gradient-to-br from-purple-500 to-purple-700
```

### Green Gradient
```css
bg-gradient-to-br from-green-500 to-green-700
```

---

## ✨ Special Effects

### Glass Morphism
```css
bg-white bg-opacity-90 backdrop-blur-lg
```

### Shadow Layers
```css
shadow-sm    - Subtle shadow
shadow-md    - Medium shadow
shadow-lg    - Large shadow
shadow-xl    - Extra large shadow
shadow-2xl   - 2X large shadow
```

### Border Styles
```css
border       - 1px border
border-2     - 2px border
border-4     - 4px border
border-dashed - Dashed border
```

---

## 🎯 Best Practices

1. **Consistency**: Use the same spacing, colors, and typography throughout
2. **Accessibility**: Ensure sufficient color contrast (WCAG AA)
3. **Performance**: Optimize images and use lazy loading
4. **Responsive**: Test on mobile, tablet, and desktop
5. **Hover States**: Always provide visual feedback on interactive elements
6. **Loading States**: Show loading indicators for async operations
7. **Empty States**: Design meaningful empty states for lists
8. **Error States**: Provide clear error messages and recovery options
9. **Focus States**: Ensure keyboard navigation works properly
10. **Semantic HTML**: Use proper HTML5 semantic elements

---

**Design System Version**: 1.0
**Last Updated**: May 2026

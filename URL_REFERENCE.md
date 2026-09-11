# BeautyBloom - URL Reference Guide

## 📍 Complete URL Structure

### Store URLs (Root `/`)
```python
# Home
'home'                    → /

# Search
'search'                  → /search/

# Category List (by type)
'category_list'           → /shop/<category_type>/
# Example: /shop/makeup/, /shop/face/, /shop/hair/

# Subcategory List
'subcategory_list'        → /category/<cat_slug>/
# Example: /category/face-cleansers/

# Product List
'product_list'            → /subcategory/<subcat_slug>/
# Example: /subcategory/face-cleansers-facial-cleanser/

# Product Detail
'product_detail'          → /product/<slug>/
# Example: /product/cerave-hydrating-facial-cleanser/
```

### Cart URLs (`/cart/`)
```python
# View Cart
'cart'                    → /cart/

# Add to Cart
'add_to_cart'             → /cart/add/<product_id>/

# Update Cart Item
'update_cart'             → /cart/update/<item_id>/

# Remove from Cart
'remove_from_cart'        → /cart/remove/<item_id>/
```

### Wishlist URLs (`/wishlist/`)
```python
# View Wishlist
'wishlist'                → /wishlist/

# Toggle Wishlist (Add/Remove)
'toggle_wishlist'         → /wishlist/toggle/<product_id>/
```

### Order URLs (`/orders/`)
```python
# Checkout
'checkout'                → /orders/checkout/

# Order Confirmation
'order_confirmation'      → /orders/confirmation/<order_id>/

# Order List (My Orders)
'order_list'              → /orders/my-orders/

# Order Detail
'order_detail'            → /orders/<order_id>/

# Cancel Order
'cancel_order'            → /orders/<order_id>/cancel/

# Order Invoice
'order_invoice'           → /orders/<order_id>/invoice/
```

### User URLs (`/users/`)
```python
# Register
'register'                → /users/register/

# Login
'login'                   → /users/login/

# Logout
'logout'                  → /users/logout/

# Profile
'profile'                 → /users/profile/
```

### Admin URL
```python
# Admin Panel
admin:index               → /admin/
```

---

## 🔗 URL Usage in Templates

### Navigation Links
```django
<!-- Home -->
<a href="{% url 'home' %}">Home</a>

<!-- Search -->
<a href="{% url 'search' %}">Shop All</a>

<!-- Category by Type -->
<a href="{% url 'category_list' 'makeup' %}">Makeup</a>
<a href="{% url 'category_list' 'face' %}">Skincare</a>
<a href="{% url 'category_list' 'hair' %}">Haircare</a>

<!-- User Links -->
<a href="{% url 'login' %}">Login</a>
<a href="{% url 'register' %}">Register</a>
<a href="{% url 'profile' %}">Profile</a>
<a href="{% url 'logout' %}">Logout</a>

<!-- Cart & Wishlist -->
<a href="{% url 'cart' %}">Cart</a>
<a href="{% url 'wishlist' %}">Wishlist</a>

<!-- Orders -->
<a href="{% url 'order_list' %}">My Orders</a>
```

### Product Links
```django
<!-- Category Link (from category object) -->
<a href="{% url 'subcategory_list' category.slug %}">{{ category.name }}</a>

<!-- Subcategory Link (from subcategory object) -->
<a href="{% url 'product_list' subcategory.slug %}">{{ subcategory.name }}</a>

<!-- Product Link (from product object) -->
<a href="{% url 'product_detail' product.slug %}">{{ product.name }}</a>
```

### Form Actions
```django
<!-- Add to Cart Form -->
<form method="post" action="{% url 'add_to_cart' product.id %}">
  {% csrf_token %}
  <!-- form fields -->
</form>

<!-- Update Cart Form -->
<form method="post" action="{% url 'update_cart' item.id %}">
  {% csrf_token %}
  <!-- form fields -->
</form>

<!-- Remove from Cart Form -->
<form method="post" action="{% url 'remove_from_cart' item.id %}">
  {% csrf_token %}
  <button type="submit">Remove</button>
</form>

<!-- Toggle Wishlist Form -->
<form method="post" action="{% url 'toggle_wishlist' product.id %}">
  {% csrf_token %}
  <button type="submit">Add to Wishlist</button>
</form>

<!-- Checkout Form -->
<form method="post" action="{% url 'checkout' %}">
  {% csrf_token %}
  <!-- form fields -->
</form>

<!-- Cancel Order Form -->
<form method="post" action="{% url 'cancel_order' order.id %}">
  {% csrf_token %}
  <button type="submit">Cancel Order</button>
</form>
```

### Order Links
```django
<!-- Order Confirmation -->
<a href="{% url 'order_confirmation' order.id %}">View Confirmation</a>

<!-- Order Detail -->
<a href="{% url 'order_detail' order.id %}">View Order</a>

<!-- Order Invoice -->
<a href="{% url 'order_invoice' order.id %}" target="_blank">Download Invoice</a>
```

---

## 🔍 Search URLs

### Search with Query Parameter
```django
<!-- Search Form -->
<form action="{% url 'search' %}" method="get">
  <input type="search" name="q" placeholder="Search...">
  <button type="submit">Search</button>
</form>

<!-- Search Link with Query -->
<a href="{% url 'search' %}?q=lipstick">Search Lipstick</a>
```

---

## 🎯 Category Type Values

Based on your models, the valid `category_type` values are:
- `face` - Face Care
- `body` - Body Care
- `hair` - Hair Care
- `makeup` - Makeup
- `wellness` - Wellness

### Usage Example
```django
<a href="{% url 'category_list' 'makeup' %}">Makeup</a>
<a href="{% url 'category_list' 'face' %}">Face Care</a>
<a href="{% url 'category_list' 'hair' %}">Hair Care</a>
<a href="{% url 'category_list' 'body' %}">Body Care</a>
<a href="{% url 'category_list' 'wellness' %}">Wellness</a>
```

---

## 🔐 Authentication URLs

### Login/Logout
```django
<!-- Login Page -->
<a href="{% url 'login' %}">Login</a>

<!-- Logout (POST request recommended) -->
<a href="{% url 'logout' %}">Logout</a>

<!-- Or with form -->
<form method="post" action="{% url 'logout' %}">
  {% csrf_token %}
  <button type="submit">Logout</button>
</form>
```

### Registration
```django
<!-- Register Page -->
<a href="{% url 'register' %}">Create Account</a>
```

### Profile
```django
<!-- User Profile -->
<a href="{% url 'profile' %}">My Account</a>
```

---

## 🛡️ Protected URLs (Login Required)

These URLs require user authentication:
- `profile` - User profile page
- `wishlist` - User wishlist
- `checkout` - Checkout page
- `order_list` - User orders
- `order_detail` - Order details
- `order_confirmation` - Order confirmation
- `cancel_order` - Cancel order
- `order_invoice` - Order invoice

### Handling in Views
```python
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # View code
    pass
```

---

## 📝 URL Parameters

### Required Parameters

#### Product ID
```django
{% url 'add_to_cart' product.id %}
{% url 'toggle_wishlist' product.id %}
```

#### Item ID (Cart Item)
```django
{% url 'update_cart' item.id %}
{% url 'remove_from_cart' item.id %}
```

#### Order ID
```django
{% url 'order_detail' order.id %}
{% url 'order_confirmation' order.id %}
{% url 'cancel_order' order.id %}
{% url 'order_invoice' order.id %}
```

#### Slug Parameters
```django
{% url 'subcategory_list' category.slug %}
{% url 'product_list' subcategory.slug %}
{% url 'product_detail' product.slug %}
```

#### Category Type
```django
{% url 'category_list' 'makeup' %}
{% url 'category_list' category.category_type %}
```

---

## 🔄 Redirect URLs

### After Login
```python
# In settings.py
LOGIN_REDIRECT_URL = '/'  # or 'home'
```

### After Logout
```python
# In settings.py
LOGOUT_REDIRECT_URL = '/'  # or 'home'
```

### After Registration
```python
# In views.py
return redirect('home')  # or 'login'
```

---

## 🚨 Common URL Errors & Fixes

### Error: NoReverseMatch
**Cause**: URL name doesn't exist or wrong parameters

**Fix**:
1. Check URL name in `urls.py`
2. Verify required parameters are provided
3. Check spelling and case sensitivity

### Error: Reverse for 'url_name' not found
**Cause**: URL pattern not defined

**Fix**:
1. Add URL pattern to appropriate `urls.py`
2. Include app URLs in main `urls.py`
3. Check URL name matches exactly

### Error: Missing required parameter
**Cause**: URL requires parameter but not provided

**Fix**:
```django
<!-- Wrong -->
{% url 'product_detail' %}

<!-- Correct -->
{% url 'product_detail' product.slug %}
```

---

## 📋 URL Testing Checklist

- [ ] All navigation links work
- [ ] Product links work
- [ ] Category links work
- [ ] Cart operations work
- [ ] Wishlist operations work
- [ ] Order links work
- [ ] User authentication links work
- [ ] Form actions submit correctly
- [ ] Search functionality works
- [ ] Admin panel accessible

---

## 🔧 URL Configuration Files

### Main URLs (`ecommerce/urls.py`)
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### App URLs
- `store/urls.py` - Store URLs
- `users/urls.py` - User URLs
- `cart/urls.py` - Cart URLs
- `wishlist/urls.py` - Wishlist URLs
- `orders/urls.py` - Order URLs

---

**Last Updated**: May 2026

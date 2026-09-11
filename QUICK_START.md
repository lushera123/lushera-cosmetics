# BeautyBloom - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.0+
- pip (Python package manager)
- Virtual environment (recommended)

---

## 📦 Installation

### 1. Clone the Repository (if applicable)
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install Django:
```bash
pip install django pillow
```

### 4. Environment Variables
Create a `.env` file in the project root (copy from `.env.example`):
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
# If you have fixtures
python manage.py loaddata categories
python manage.py loaddata products
```

### 7. Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 🗂️ Project Structure

```
project/
├── ecommerce/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                  # Store app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── cart/                   # Cart app
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── wishlist/               # Wishlist app
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── orders/                 # Orders app
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── users/                  # Users app (if separate)
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/              # HTML templates
│   ├── base.html
│   ├── store/
│   ├── cart/
│   ├── wishlist/
│   ├── orders/
│   └── users/
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                  # User uploaded files
│   ├── categories/
│   ├── subcategories/
│   └── products/
├── manage.py
├── requirements.txt
└── .env
```

---

## 🔧 Configuration

### Settings (`ecommerce/settings.py`)

#### Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'cart',
    'wishlist',
    'orders',
    'chatbot',  # if applicable
]
```

#### Templates
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_count',  # Add this
            ],
        },
    },
]
```

#### Static Files
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### URLs (`ecommerce/urls.py`)
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/Logout
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 📊 Admin Panel

### Access Admin Panel
1. Create superuser (if not done):
   ```bash
   python manage.py createsuperuser
   ```

2. Visit: http://127.0.0.1:8000/admin/

3. Login with superuser credentials

### Add Sample Data

#### Categories
1. Go to Store > Categories
2. Click "Add Category"
3. Fill in:
   - Name: e.g., "Cleansers"
   - Category Type: e.g., "Face Care"
   - Upload image
   - Add description
4. Save

#### Subcategories
1. Go to Store > SubCategories
2. Click "Add SubCategory"
3. Fill in:
   - Category: Select parent category
   - Name: e.g., "Facial Cleanser"
   - Upload image
4. Save

#### Products
1. Go to Store > Products
2. Click "Add Product"
3. Fill in:
   - Subcategory: Select subcategory
   - Name: e.g., "CeraVe Hydrating Facial Cleanser"
   - Description: Product details
   - Price: e.g., 2500
   - Discount Price: e.g., 2000 (optional)
   - Stock: e.g., 50
   - Upload image
   - Tag: e.g., "New Arrival"
4. Save

#### Product Variants (Optional)
1. Go to Store > Product Variants
2. Click "Add Product Variant"
3. Fill in:
   - Product: Select product
   - Size: e.g., "100ml"
   - Color: e.g., "Unscented"
   - Stock: e.g., 20
4. Save

---

## 🎨 Customization

### Change Brand Name
1. Open `templates/base.html`
2. Find "BeautyBloom" and replace with your brand name
3. Update logo if needed

### Change Colors
1. Open `templates/base.html`
2. Find the Tailwind config section:
   ```javascript
   tailwind.config = {
     theme: {
       extend: {
         colors: {
           rose: '#FF6B9D',  // Change this
           // ... other colors
         }
       }
     }
   }
   ```

### Change Fonts
1. Open `templates/base.html`
2. Find Google Fonts link
3. Replace with your preferred fonts
4. Update Tailwind config

### Add Custom CSS
1. Create `static/css/custom.css`
2. Add your custom styles
3. Include in `base.html`:
   ```html
   {% block extra_css %}
   <link rel="stylesheet" href="{% static 'css/custom.css' %}">
   {% endblock %}
   ```

---

## 🔗 URL Patterns

### Store URLs
```
/                          - Home page
/search/                   - Search page
/category/<slug>/          - Category list
/subcategory/<slug>/       - Subcategory list
/products/<slug>/          - Product list
/product/<slug>/           - Product detail
```

### Cart URLs
```
/cart/                     - View cart
/cart/add/<id>/            - Add to cart
/cart/update/<id>/         - Update cart item
/cart/remove/<id>/         - Remove from cart
```

### Wishlist URLs
```
/wishlist/                 - View wishlist
/wishlist/toggle/<id>/     - Add/Remove from wishlist
```

### Order URLs
```
/orders/                   - Order list
/orders/<id>/              - Order detail
/orders/checkout/          - Checkout
/orders/confirmation/<id>/ - Order confirmation
/orders/cancel/<id>/       - Cancel order
/orders/invoice/<id>/      - Order invoice
```

### User URLs
```
/accounts/login/           - Login
/accounts/logout/          - Logout
/accounts/register/        - Register
/accounts/profile/         - User profile
/accounts/password/change/ - Change password
/accounts/password/reset/  - Reset password
```

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test store
python manage.py test cart
```

### Check for Issues
```bash
python manage.py check
```

---

## 🐛 Troubleshooting

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Check STATIC_URL and STATIC_ROOT in settings.py
```

### Images Not Displaying
```bash
# Check MEDIA_URL and MEDIA_ROOT in settings.py
# Ensure media files are in correct directory
# Check URLs configuration includes static/media URLs
```

### Template Not Found
```bash
# Check TEMPLATES DIRS in settings.py
# Ensure template path is correct
# Check template name in view
```

### Database Errors
```bash
# Delete db.sqlite3
# Delete all migration files (except __init__.py)
# Run migrations again
python manage.py makemigrations
python manage.py migrate
```

### Import Errors
```bash
# Ensure all apps are in INSTALLED_APPS
# Check import statements in views.py
# Verify app structure
```

---

## 📚 Resources

### Documentation
- Django: https://docs.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/docs
- Alpine.js: https://alpinejs.dev/

### Design Resources
- Heroicons: https://heroicons.com/
- Google Fonts: https://fonts.google.com/
- Unsplash (Images): https://unsplash.com/

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Use production database (PostgreSQL)
- [ ] Collect static files
- [ ] Set up media file storage
- [ ] Configure HTTPS
- [ ] Set up email backend
- [ ] Enable CSRF protection
- [ ] Set up logging
- [ ] Configure caching
- [ ] Set up backup system

### Deployment Platforms
- **Heroku**: Easy deployment with Git
- **DigitalOcean**: VPS with more control
- **AWS**: Scalable cloud hosting
- **PythonAnywhere**: Simple Python hosting
- **Railway**: Modern deployment platform

---

## 💡 Tips

1. **Use Virtual Environment**: Always activate virtual environment before working
2. **Commit Often**: Use Git to track changes
3. **Test Locally**: Test all features before deploying
4. **Backup Database**: Regular backups of production database
5. **Monitor Logs**: Check logs for errors and issues
6. **Optimize Images**: Compress images before uploading
7. **Use CDN**: Use CDN for static files in production
8. **Cache Queries**: Cache expensive database queries
9. **Security**: Keep Django and dependencies updated
10. **Documentation**: Document custom features and changes

---

## 📞 Support

### Getting Help
- Django Documentation: https://docs.djangoproject.com/
- Stack Overflow: https://stackoverflow.com/questions/tagged/django
- Django Forum: https://forum.djangoproject.com/
- Reddit: r/django

---

**Happy Coding! 🎉**

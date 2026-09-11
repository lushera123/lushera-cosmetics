"""
Run this once to create an admin user:
  python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from users.models import User

if not User.objects.filter(email='admin@glowcare.com').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@glowcare.com',
        password='admin123'
    )
    print('Superuser created: admin@glowcare.com / admin123')
else:
    print('Superuser already exists.')

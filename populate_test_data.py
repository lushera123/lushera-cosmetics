import os
import django
from django.core.files import File
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Category, SubCategory, Product, ProductVariant

# Clear existing data
ProductVariant.objects.all().delete()
Product.objects.all().delete()
SubCategory.objects.all().delete()
Category.objects.all().delete()

print("Creating categories...")

# Wellness Category
wellness_cat = Category.objects.create(
    name='Wellness',
    category_type='wellness',
    description='Wellness and self-care products'
)

# Check if category images exist
cat_image_path = Path('media/categories/cat_wellness_Sunscreen.jpg')
if cat_image_path.exists():
    with open(cat_image_path, 'rb') as f:
        wellness_cat.image.save('cat_wellness_Sunscreen.jpg', File(f), save=True)
    print(f"✓ Added image to {wellness_cat.name}")

# Wellness Subcategories
sunscreen_sub = SubCategory.objects.create(
    category=wellness_cat,
    name='Sunscreen'
)

sub_image_path = Path('media/subcategories/sub_Sunscreen.jpg')
if sub_image_path.exists():
    with open(sub_image_path, 'rb') as f:
        sunscreen_sub.image.save('sub_Sunscreen.jpg', File(f), save=True)

essential_oils_sub = SubCategory.objects.create(
    category=wellness_cat,
    name='Essential Oils'
)

sub_image_path2 = Path('media/subcategories/sub_Essential_Oils.jpg')
if sub_image_path2.exists():
    with open(sub_image_path2, 'rb') as f:
        essential_oils_sub.image.save('sub_Essential_Oils.jpg', File(f), save=True)

face_masks_sub = SubCategory.objects.create(
    category=wellness_cat,
    name='Face Masks'
)

sub_image_path3 = Path('media/subcategories/sub_Face_Masks.jpg')
if sub_image_path3.exists():
    with open(sub_image_path3, 'rb') as f:
        face_masks_sub.image.save('sub_Face_Masks.jpg', File(f), save=True)

print("Creating products with variants...")

# Product 1: Himalaya Sunscreen with different prices for each size
himalaya = Product.objects.create(
    subcategory=sunscreen_sub,
    name='Himalaya Sunscreen SPF 50',
    description='Beautifully tailored with chikankari embroidery. A must-have for the festive season.',
    price=500,
    discount_price=400,
    stock=0,  # Stock will be in variants
    tag='new'
)

# Try to add product image
prod_image_path = Path('media/products/prod_Himalaya_Sunscreen.jpg')
if prod_image_path.exists():
    with open(prod_image_path, 'rb') as f:
        himalaya.image.save('prod_Himalaya_Sunscreen.jpg', File(f), save=True)
else:
    # Use any available product image as fallback
    available_images = list(Path('media/products').glob('*.jpg'))
    if available_images:
        with open(available_images[0], 'rb') as f:
            himalaya.image.save(available_images[0].name, File(f), save=True)

# Variants with different prices
ProductVariant.objects.create(product=himalaya, size='30ml', stock=5, price=200, discount_price=150)
ProductVariant.objects.create(product=himalaya, size='50ml', stock=8, price=300, discount_price=250)
ProductVariant.objects.create(product=himalaya, size='100ml', stock=10, price=500, discount_price=400)
ProductVariant.objects.create(product=himalaya, size='150ml', stock=7, price=700, discount_price=600)
ProductVariant.objects.create(product=himalaya, size='200ml', stock=6, price=900, discount_price=750)
ProductVariant.objects.create(product=himalaya, size='250ml', stock=4, price=1100, discount_price=900)
ProductVariant.objects.create(product=himalaya, size='500ml', stock=3, price=1800, discount_price=1500)
ProductVariant.objects.create(product=himalaya, size='1L', stock=2, price=3000, discount_price=2500)

print(f"✓ Created {himalaya.name} with 8 variants")

# Get all available product images for other products
available_images = list(Path('media/products').glob('*.jpg'))

# Product 2: Lavender Essential Oil
lavender = Product.objects.create(
    subcategory=essential_oils_sub,
    name='Pure Lavender Essential Oil',
    description='Premium quality lavender oil for relaxation and aromatherapy. 100% natural and organic.',
    price=800,
    discount_price=650,
    stock=0,
    tag='best_seller'
)

if len(available_images) > 1:
    with open(available_images[1], 'rb') as f:
        lavender.image.save(available_images[1].name, File(f), save=True)

ProductVariant.objects.create(product=lavender, size='30ml', stock=10, price=400, discount_price=350)
ProductVariant.objects.create(product=lavender, size='50ml', stock=8, price=600, discount_price=500)
ProductVariant.objects.create(product=lavender, size='100ml', stock=5, price=1000, discount_price=800)

print(f"✓ Created {lavender.name} with 3 variants")

# Product 3: Tea Tree Oil
teatree = Product.objects.create(
    subcategory=essential_oils_sub,
    name='Tea Tree Essential Oil',
    description='Natural tea tree oil with antibacterial properties. Perfect for skincare.',
    price=700,
    discount_price=600,
    stock=0,
    tag='sale'
)

if len(available_images) > 2:
    with open(available_images[2], 'rb') as f:
        teatree.image.save(available_images[2].name, File(f), save=True)

ProductVariant.objects.create(product=teatree, size='30ml', stock=12, price=350, discount_price=300)
ProductVariant.objects.create(product=teatree, size='50ml', stock=10, price=550, discount_price=450)
ProductVariant.objects.create(product=teatree, size='100ml', stock=6, price=900, discount_price=700)

print(f"✓ Created {teatree.name} with 3 variants")

# Product 4: Charcoal Face Mask
charcoal = Product.objects.create(
    subcategory=face_masks_sub,
    name='Activated Charcoal Face Mask',
    description='Deep cleansing charcoal mask that removes impurities and toxins.',
    price=600,
    discount_price=500,
    stock=0,
    tag='featured'
)

if len(available_images) > 3:
    with open(available_images[3], 'rb') as f:
        charcoal.image.save(available_images[3].name, File(f), save=True)

ProductVariant.objects.create(product=charcoal, size='50ml', stock=15, price=300, discount_price=250)
ProductVariant.objects.create(product=charcoal, size='100ml', stock=12, price=500, discount_price=400)
ProductVariant.objects.create(product=charcoal, size='200ml', stock=8, price=900, discount_price=750)

print(f"✓ Created {charcoal.name} with 3 variants")

# Product 5: Aloe Vera Sunscreen
aloe = Product.objects.create(
    subcategory=sunscreen_sub,
    name='Aloe Vera Sunscreen SPF 30',
    description='Lightweight sunscreen with aloe vera for sensitive skin.',
    price=450,
    discount_price=350,
    stock=0,
    tag='new'
)

if len(available_images) > 4:
    with open(available_images[4], 'rb') as f:
        aloe.image.save(available_images[4].name, File(f), save=True)

ProductVariant.objects.create(product=aloe, size='50ml', stock=10, price=250, discount_price=200)
ProductVariant.objects.create(product=aloe, size='100ml', stock=8, price=400, discount_price=320)
ProductVariant.objects.create(product=aloe, size='150ml', stock=5, price=600, discount_price=480)

print(f"✓ Created {aloe.name} with 3 variants")

print("\n" + "="*50)
print("✅ Test data created successfully!")
print("="*50)
print(f"Categories: {Category.objects.count()}")
print(f"SubCategories: {SubCategory.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Variants: {ProductVariant.objects.count()}")
print("\nLogin: admin@glowcare.com / admin123")
print("\nServer: http://127.0.0.1:8000")


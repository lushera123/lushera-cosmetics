import os
import django
from django.core.files import File
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Category, SubCategory, Product, ProductVariant

# Clear existing data
print("Clearing existing data...")
ProductVariant.objects.all().delete()
Product.objects.all().delete()
SubCategory.objects.all().delete()
Category.objects.all().delete()

print("\n" + "="*60)
print("CREATING COMPREHENSIVE TEST DATA")
print("="*60)

# Get available images
categories_path = Path('media/categories')
subcategories_path = Path('media/subcategories')
products_path = Path('media/products')

category_images = {img.stem.replace('cat_', ''): img for img in categories_path.glob('*.jpg')} if categories_path.exists() else {}
subcategory_images = {img.stem.replace('sub_', ''): img for img in subcategories_path.glob('*.jpg')} if subcategories_path.exists() else {}
product_images = list(products_path.glob('*.jpg')) if products_path.exists() else []

print(f"\nFound {len(category_images)} category images")
print(f"Found {len(subcategory_images)} subcategory images")
print(f"Found {len(product_images)} product images")

product_img_index = 0

def get_next_product_image():
    global product_img_index
    if product_images:
        img = product_images[product_img_index % len(product_images)]
        product_img_index += 1
        return img
    return None

# ============================================================================
# MAKEUP CATEGORY
# ============================================================================
print("\n📦 Creating MAKEUP category...")
makeup_cat = Category.objects.create(
    name='Makeup',
    category_type='makeup',
    description='Professional makeup products for every look'
)

# Add category image
cat_img_key = 'makeup_Foundation'
if cat_img_key in category_images:
    with open(category_images[cat_img_key], 'rb') as f:
        makeup_cat.image.save(category_images[cat_img_key].name, File(f), save=True)

# Makeup Subcategories
foundation_sub = SubCategory.objects.create(category=makeup_cat, name='Foundation')
lipstick_sub = SubCategory.objects.create(category=makeup_cat, name='Lipstick')
mascara_sub = SubCategory.objects.create(category=makeup_cat, name='Mascara')

# Add subcategory images
for sub, key in [(foundation_sub, 'Foundation'), (lipstick_sub, 'Lipstick'), (mascara_sub, 'Mascara')]:
    if key in subcategory_images:
        with open(subcategory_images[key], 'rb') as f:
            sub.image.save(subcategory_images[key].name, File(f), save=True)

# Foundation Products
products_data = [
    ('Matte Finish Foundation', 'Long-lasting matte foundation for flawless coverage', 1200, 999, 'best_seller'),
    ('Dewy Glow Foundation', 'Hydrating foundation with natural glow finish', 1400, 1199, 'new'),
    ('Full Coverage Foundation', 'Professional full coverage foundation', 1600, 1399, 'featured'),
]

for name, desc, price, disc, tag in products_data:
    prod = Product.objects.create(
        subcategory=foundation_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    # Add variants
    ProductVariant.objects.create(product=prod, size='30ml', stock=15, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='50ml', stock=10, price=price+200, discount_price=disc+150)

print(f"  ✓ Created {foundation_sub.name} with {foundation_sub.products.count()} products")

# Lipstick Products
lipstick_data = [
    ('Matte Lipstick - Red', 'Bold matte red lipstick', 800, 650, 'sale'),
    ('Glossy Lipstick - Pink', 'Shiny pink lipstick with moisturizing formula', 900, 750, 'new'),
    ('Nude Lipstick', 'Perfect nude shade for everyday wear', 850, 700, 'best_seller'),
]

for name, desc, price, disc, tag in lipstick_data:
    prod = Product.objects.create(
        subcategory=lipstick_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='30ml', stock=20, price=price, discount_price=disc)

print(f"  ✓ Created {lipstick_sub.name} with {lipstick_sub.products.count()} products")

# ============================================================================
# FACE CARE CATEGORY
# ============================================================================
print("\n🧴 Creating FACE CARE category...")
face_cat = Category.objects.create(
    name='Face Care',
    category_type='face',
    description='Complete skincare solutions for healthy skin'
)

cat_img_key = 'face_Cleansers'
if cat_img_key in category_images:
    with open(category_images[cat_img_key], 'rb') as f:
        face_cat.image.save(category_images[cat_img_key].name, File(f), save=True)

# Face Care Subcategories
cleanser_sub = SubCategory.objects.create(category=face_cat, name='Cleansers')
moisturizer_sub = SubCategory.objects.create(category=face_cat, name='Moisturizers')
serum_sub = SubCategory.objects.create(category=face_cat, name='Serums')

# Add subcategory images
for sub, key in [(cleanser_sub, 'Facial_Cleanser'), (moisturizer_sub, 'Face_Cream'), (serum_sub, 'Face_Cream')]:
    if key in subcategory_images:
        with open(subcategory_images[key], 'rb') as f:
            sub.image.save(subcategory_images[key].name, File(f), save=True)

# Cleanser Products
cleanser_data = [
    ('Gentle Foaming Cleanser', 'Mild cleanser for all skin types', 600, 499, 'new'),
    ('Deep Cleansing Face Wash', 'Deep pore cleansing formula', 700, 599, 'best_seller'),
    ('Hydrating Cleanser', 'Moisturizing cleanser for dry skin', 650, 549, 'featured'),
]

for name, desc, price, disc, tag in cleanser_data:
    prod = Product.objects.create(
        subcategory=cleanser_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='100ml', stock=25, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='200ml', stock=15, price=price+300, discount_price=disc+250)

print(f"  ✓ Created {cleanser_sub.name} with {cleanser_sub.products.count()} products")

# Moisturizer Products
moisturizer_data = [
    ('Day Cream SPF 30', 'Daily moisturizer with sun protection', 1100, 899, 'best_seller'),
    ('Night Repair Cream', 'Intensive overnight moisturizer', 1300, 1099, 'new'),
    ('Gel Moisturizer', 'Lightweight gel for oily skin', 950, 799, 'sale'),
]

for name, desc, price, disc, tag in moisturizer_data:
    prod = Product.objects.create(
        subcategory=moisturizer_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='50ml', stock=20, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='100ml', stock=12, price=price+400, discount_price=disc+350)

print(f"  ✓ Created {moisturizer_sub.name} with {moisturizer_sub.products.count()} products")

# ============================================================================
# HAIR CARE CATEGORY
# ============================================================================
print("\n💇 Creating HAIR CARE category...")
hair_cat = Category.objects.create(
    name='Hair Care',
    category_type='hair',
    description='Professional hair care products'
)

cat_img_key = 'hair_Shampoo'
if cat_img_key in category_images:
    with open(category_images[cat_img_key], 'rb') as f:
        hair_cat.image.save(category_images[cat_img_key].name, File(f), save=True)

# Hair Care Subcategories
shampoo_sub = SubCategory.objects.create(category=hair_cat, name='Shampoo')
conditioner_sub = SubCategory.objects.create(category=hair_cat, name='Conditioner')
hair_oil_sub = SubCategory.objects.create(category=hair_cat, name='Hair Oil')

# Add subcategory images
for sub, key in [(shampoo_sub, 'Shampoo'), (conditioner_sub, 'Conditioner'), (hair_oil_sub, 'Hair_Oil')]:
    if key in subcategory_images:
        with open(subcategory_images[key], 'rb') as f:
            sub.image.save(subcategory_images[key].name, File(f), save=True)

# Shampoo Products
shampoo_data = [
    ('Anti-Dandruff Shampoo', 'Effective dandruff control shampoo', 550, 449, 'best_seller'),
    ('Volumizing Shampoo', 'Adds volume and bounce to hair', 600, 499, 'new'),
    ('Repair Shampoo', 'Repairs damaged hair', 650, 549, 'featured'),
]

for name, desc, price, disc, tag in shampoo_data:
    prod = Product.objects.create(
        subcategory=shampoo_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='200ml', stock=30, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='500ml', stock=20, price=price+400, discount_price=disc+350)

print(f"  ✓ Created {shampoo_sub.name} with {shampoo_sub.products.count()} products")

# Hair Oil Products
hair_oil_data = [
    ('Coconut Hair Oil', 'Pure coconut oil for hair nourishment', 400, 349, 'best_seller'),
    ('Argan Hair Oil', 'Moroccan argan oil for shine', 800, 699, 'new'),
]

for name, desc, price, disc, tag in hair_oil_data:
    prod = Product.objects.create(
        subcategory=hair_oil_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='100ml', stock=25, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='200ml', stock=15, price=price+250, discount_price=disc+200)

print(f"  ✓ Created {hair_oil_sub.name} with {hair_oil_sub.products.count()} products")

# ============================================================================
# WELLNESS CATEGORY
# ============================================================================
print("\n🌿 Creating WELLNESS category...")
wellness_cat = Category.objects.create(
    name='Wellness',
    category_type='wellness',
    description='Wellness and self-care products'
)

cat_img_key = 'wellness_Sunscreen'
if cat_img_key in category_images:
    with open(category_images[cat_img_key], 'rb') as f:
        wellness_cat.image.save(category_images[cat_img_key].name, File(f), save=True)

# Wellness Subcategories
sunscreen_sub = SubCategory.objects.create(category=wellness_cat, name='Sunscreen')
essential_oils_sub = SubCategory.objects.create(category=wellness_cat, name='Essential Oils')
face_masks_sub = SubCategory.objects.create(category=wellness_cat, name='Face Masks')

# Add subcategory images
for sub, key in [(sunscreen_sub, 'Sunscreen'), (essential_oils_sub, 'Essential_Oils'), (face_masks_sub, 'Face_Masks')]:
    if key in subcategory_images:
        with open(subcategory_images[key], 'rb') as f:
            sub.image.save(subcategory_images[key].name, File(f), save=True)

# Sunscreen Products
sunscreen_data = [
    ('SPF 50 Sunscreen', 'High protection sunscreen', 700, 599, 'best_seller'),
    ('SPF 30 Daily Sunscreen', 'Everyday sun protection', 550, 449, 'new'),
    ('Tinted Sunscreen SPF 40', 'Sunscreen with light tint', 850, 699, 'featured'),
]

for name, desc, price, disc, tag in sunscreen_data:
    prod = Product.objects.create(
        subcategory=sunscreen_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='50ml', stock=20, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='100ml', stock=15, price=price+300, discount_price=disc+250)

print(f"  ✓ Created {sunscreen_sub.name} with {sunscreen_sub.products.count()} products")

# Essential Oils Products
essential_oils_data = [
    ('Lavender Essential Oil', 'Calming lavender oil', 600, 499, 'best_seller'),
    ('Tea Tree Essential Oil', 'Antibacterial tea tree oil', 550, 449, 'new'),
    ('Peppermint Essential Oil', 'Refreshing peppermint oil', 500, 399, 'sale'),
]

for name, desc, price, disc, tag in essential_oils_data:
    prod = Product.objects.create(
        subcategory=essential_oils_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='30ml', stock=25, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='50ml', stock=15, price=price+200, discount_price=disc+150)

print(f"  ✓ Created {essential_oils_sub.name} with {essential_oils_sub.products.count()} products")

# Face Masks Products
face_masks_data = [
    ('Charcoal Face Mask', 'Deep cleansing charcoal mask', 450, 349, 'best_seller'),
    ('Hydrating Sheet Mask', 'Moisturizing sheet mask', 300, 249, 'new'),
]

for name, desc, price, disc, tag in face_masks_data:
    prod = Product.objects.create(
        subcategory=face_masks_sub, name=name, description=desc,
        price=price, discount_price=disc, stock=0, tag=tag
    )
    img = get_next_product_image()
    if img:
        with open(img, 'rb') as f:
            prod.image.save(img.name, File(f), save=True)
    
    ProductVariant.objects.create(product=prod, size='50ml', stock=30, price=price, discount_price=disc)
    ProductVariant.objects.create(product=prod, size='100ml', stock=20, price=price+200, discount_price=disc+150)

print(f"  ✓ Created {face_masks_sub.name} with {face_masks_sub.products.count()} products")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("✅ DATA CREATION COMPLETE!")
print("="*60)
print(f"Categories: {Category.objects.count()}")
print(f"SubCategories: {SubCategory.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Variants: {ProductVariant.objects.count()}")
print("\nLogin: admin@glowcare.com / admin123")
print("Server: http://127.0.0.1:8000")
print("="*60)

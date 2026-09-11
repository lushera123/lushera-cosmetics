"""
Seeds the database with Pakistani skincare products and downloads real product images
from Unsplash (free, no API key required).

Usage:  python manage.py seed_data
        python manage.py seed_data --flush   (clears existing data first)
"""
import os
import time
import urllib.request
import urllib.error
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Category, SubCategory, Product, ProductVariant

# ---------------------------------------------------------------------------
# Unsplash "source" URLs — each resolves to a real photo, no API key needed.
# Format: https://source.unsplash.com/<photo_id>/800x1000
# All photos are free to use (Unsplash licence).
# ---------------------------------------------------------------------------

# Category hero images
CAT_IMAGES = {
    'face':     'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80',  # skincare products
    'body':     'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',  # body lotion
    'hair':     'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=800&q=80',  # shampoo bottles
    'makeup':   'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=80',  # makeup products
    'wellness': 'https://images.unsplash.com/photo-1505944270255-72b8c68c6a70?w=800&q=80',  # essential oils
}

# Subcategory images (Pakistani skincare types)
SUBCAT_IMAGES = {
    'cleansers':        'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600&q=80',
    'moisturizers':     'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&q=80',
    'serums':          'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=600&q=80',
    'sunscreen':       'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=600&q=80',
    'body_lotion':     'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=600&q=80',
    'body_wash':       'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600&q=80',
    'shampoo':         'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=600&q=80',
    'conditioner':     'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=600&q=80',
    'hair_oil':        'https://images.unsplash.com/photo-1505944270255-72b8c68c6a70?w=600&q=80',
    'foundation':      'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&q=80',
    'lipstick':        'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&q=80',
    'mascara':         'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&q=80',
    'essential_oils':  'https://images.unsplash.com/photo-1505944270255-72b8c68c6a70?w=600&q=80',
    'face_masks':      'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=600&q=80',
    'default':         'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80',
}

# Product images — keyed by product name (lowercase), falls back to category pool
PRODUCT_IMAGES = {
    # The Ordinary
    'the ordinary hyaluronic acid 2% + b5': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80',
    'the ordinary niacinamide 10% + zinc 1%': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=80',
    'the ordinary vitamin c suspension 23% + ha spheres 2%': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    'the ordinary natural moisturizing factors + ha': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    # CeraVe
    'cerave moisturizing cream': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    'cerave hydrating facial cleanser': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80',
    'cerave sunscreen broad spectrum spf 50': 'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=800&q=80',
    # La Roche-Posay
    'la roche-posay toleriane double repair face moisturizer': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    'la roche-posay lipikar wash ap+': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80',
    # Garnier
    'garnier skin naturals bright complete vitamin c booster serum': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=80',
    'garnier micellar cleansing water': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80',
    # Nivea
    'nivea soft cream': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    'nivea men sensitive cooling post shave balm': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    # Pond's
    'ponds bright beauty spot-less glow cream': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    'ponds pure white anti-spot fairness cream': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    # Himalaya
    'himalaya neem face wash': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80',
    'himalaya purifying neem pack': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    # Eva
    'eva brightening night cream': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    'eva whitening day cream': 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    # Huda Beauty
    'huda beauty desert dusk blush': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=80',
    'huda beauty life liner': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=80',
}

# Fallback pool — cycled when a product has no specific image
FALLBACK_POOL = [
    'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80',
    'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=800&q=80',
    'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&q=80',
    'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=800&q=80',
    'https://images.unsplash.com/photo-1505944270255-72b8c68c6a70?w=800&q=80',
]

# ---------------------------------------------------------------------------
# Descriptions — Pakistani context
# ---------------------------------------------------------------------------
DESCRIPTIONS = [
    "Premium quality fabric with intricate embroidery. Perfect for Eid and festive occasions.",
    "Crafted from fine lawn fabric, this suit offers breathable comfort for Pakistan's warm summers.",
    "A wardrobe staple featuring traditional Pakistani craftsmanship with a modern silhouette.",
    "Elegant design with hand-stitched details. Ideal for formal gatherings and family events.",
    "Soft, lightweight cotton fabric with a classic Pakistani cut. Comfortable for daily wear.",
    "Timeless style inspired by traditional Pakistani fashion. Durable and easy to maintain.",
    "Beautifully tailored with chikankari embroidery. A must-have for the festive season.",
    "Fashion-forward design rooted in Pakistani heritage. A crowd favourite every season.",
    "Made from high-quality khaddar fabric, perfect for winter wear with a traditional touch.",
    "Vibrant digital print on premium lawn. Pairs beautifully with a matching dupatta.",
]

# ---------------------------------------------------------------------------
# Skincare volume sizes
# ---------------------------------------------------------------------------
SKINCARE_SIZES = ['30ml', '50ml', '100ml', '150ml', '200ml', '250ml', '500ml', '1L']
STOCK_MAP = {
    '30ml': 10, '50ml': 14, '100ml': 18, '150ml': 16,
    '200ml': 12, '250ml': 10, '500ml': 8, '1L': 6,
}

# ---------------------------------------------------------------------------
# Seed data — Pakistani clothing catalogue (prices in PKR)
# ---------------------------------------------------------------------------
SEED = {
    'face': {
        'Cleansers': {
            'subcategories': ['Facial Cleanser', 'Micellar Water', 'Face Wash', 'Exfoliator'],
            'products': [
                # (name, price PKR, discount_price, stock, tag)
                ('CeraVe Hydrating Facial Cleanser', 2500, None, 50, 'best_seller'),
                ('Garnier Micellar Cleansing Water', 800, 650, 80, 'sale'),
                ('Himalaya Neem Face Wash', 450, None, 100, 'new'),
                ('La Roche-Posay Toleriane Cleanser', 3200, 2800, 30, 'featured'),
                ('The Ordinary Squalane Cleanser', 1800, None, 40, 'best_seller'),
                ('Eva Brightening Face Wash', 350, 280, 60, 'sale'),
                ('Pond\'s Pure White Face Wash', 200, None, 120, 'new'),
                ('Nivea Men Sensitive Face Wash', 400, 320, 70, 'sale'),
            ],
        },
        'Moisturizers': {
            'subcategories': ['Face Cream', 'Night Cream', 'Day Cream', 'Hydrating Gel'],
            'products': [
                ('CeraVe Moisturizing Cream', 2800, None, 45, 'best_seller'),
                ('La Roche-Posay Toleriane Moisturizer', 3500, 3000, 35, 'featured'),
                ('The Ordinary Natural Moisturizing Factors', 1600, None, 60, 'new'),
                ('Nivea Soft Cream', 300, 240, 100, 'sale'),
                ('Eva Brightening Night Cream', 600, None, 80, 'best_seller'),
                ('Pond\'s Bright Beauty Cream', 250, 200, 90, 'sale'),
                ('Himalaya Nourishing Skin Cream', 400, None, 70, 'new'),
                ('Garnier Skin Naturals Moisturizer', 500, 400, 85, 'sale'),
            ],
        },
        'Serums': {
            'subcategories': ['Vitamin C Serum', 'Hyaluronic Acid', 'Niacinamide', 'Retinol'],
            'products': [
                ('The Ordinary Hyaluronic Acid 2% + B5', 2200, None, 40, 'best_seller'),
                ('The Ordinary Niacinamide 10% + Zinc 1%', 1800, 1500, 50, 'sale'),
                ('The Ordinary Vitamin C Suspension', 2000, None, 35, 'featured'),
                ('Garnier Skin Naturals Vitamin C Serum', 1200, 1000, 60, 'new'),
                ('La Roche-Posay Vitamin C Serum', 4200, None, 25, 'best_seller'),
                ('Eva Vitamin C Brightening Serum', 800, 650, 70, 'sale'),
                ('Himalaya Vitamin C Serum', 900, None, 55, 'new'),
                ('Pond\'s Vitamin C Serum', 600, 480, 80, 'sale'),
            ],
        },
    },
    'body': {
        'Body Lotion': {
            'subcategories': ['Body Lotion', 'Body Butter', 'Body Oil', 'Hand Cream'],
            'products': [
                ('Nivea Body Lotion', 400, 320, 90, 'best_seller'),
                ('CeraVe Moisturizing Body Lotion', 2200, None, 50, 'new'),
                ('Himalaya Body Lotion', 500, 400, 80, 'sale'),
                ('Eva Body Lotion', 350, None, 70, 'best_seller'),
                ('Pond\'s Body Lotion', 300, 240, 100, 'sale'),
                ('La Roche-Posay Lipikar Balm', 2800, 2400, 40, 'featured'),
                ('The Ordinary Body Oil', 1900, None, 45, 'new'),
                ('Garnier Body Lotion', 350, 280, 85, 'sale'),
            ],
        },
        'Body Wash': {
            'subcategories': ['Body Wash', 'Shower Gel', 'Soap', 'Body Scrub'],
            'products': [
                ('La Roche-Posay Lipikar Wash', 2400, None, 60, 'best_seller'),
                ('CeraVe Hydrating Body Wash', 1800, 1500, 70, 'sale'),
                ('Himalaya Neem Body Wash', 450, None, 90, 'new'),
                ('Nivea Body Wash', 350, 280, 100, 'best_seller'),
                ('Eva Body Wash', 300, None, 80, 'sale'),
                ('Pond\'s Body Wash', 250, 200, 110, 'new'),
                ('Garnier Body Wash', 400, 320, 75, 'sale'),
                ('The Ordinary Body Cleanser', 1600, None, 50, 'featured'),
            ],
        },
    },
    'hair': {
        'Shampoo': {
            'subcategories': ['Shampoo', 'Conditioner', 'Hair Oil', 'Hair Mask'],
            'products': [
                ('Himalaya Anti-Hair Fall Shampoo', 600, 480, 70, 'best_seller'),
                ('Garnier Fructis Shampoo', 450, None, 80, 'new'),
                ('Eva Hair Shampoo', 350, 280, 90, 'sale'),
                ('Pond\'s Hair Shampoo', 300, None, 100, 'best_seller'),
                ('Nivea Hair Shampoo', 400, 320, 85, 'sale'),
                ('La Roche-Posay Hair Shampoo', 2800, None, 40, 'featured'),
                ('The Ordinary Hair Shampoo', 1800, 1500, 55, 'new'),
                ('CeraVe Hair Shampoo', 2200, None, 45, 'best_seller'),
            ],
        },
        'Conditioner': {
            'subcategories': ['Conditioner', 'Hair Oil', 'Hair Serum', 'Hair Treatment'],
            'products': [
                ('Himalaya Protein Conditioner', 550, None, 75, 'best_seller'),
                ('Garnier Fructis Conditioner', 450, 360, 80, 'sale'),
                ('Eva Hair Conditioner', 350, None, 85, 'new'),
                ('Pond\'s Hair Conditioner', 300, 240, 95, 'sale'),
                ('Nivea Hair Conditioner', 400, None, 80, 'best_seller'),
                ('La Roche-Posay Hair Conditioner', 2600, 2200, 35, 'featured'),
                ('The Ordinary Hair Conditioner', 1700, None, 50, 'new'),
                ('CeraVe Hair Conditioner', 2100, 1800, 40, 'sale'),
            ],
        },
        'Hair Oil': {
            'subcategories': ['Hair Oil', 'Hair Serum', 'Scalp Treatment', 'Hair Mask'],
            'products': [
                ('Himalaya Anti-Dandruff Hair Oil', 400, None, 90, 'best_seller'),
                ('Eva Hair Oil', 300, 240, 100, 'sale'),
                ('Pond\'s Hair Oil', 250, None, 110, 'new'),
                ('Nivea Hair Oil', 350, 280, 85, 'sale'),
                ('Garnier Hair Oil', 450, None, 75, 'best_seller'),
                ('La Roche-Posay Hair Oil', 3200, 2800, 30, 'featured'),
                ('The Ordinary Hair Oil', 1900, None, 45, 'new'),
                ('CeraVe Hair Oil', 2400, 2000, 40, 'sale'),
            ],
        },
    },
    'makeup': {
        'Foundation': {
            'subcategories': ['Foundation', 'Concealer', 'BB Cream', 'CC Cream'],
            'products': [
                ('Huda Beauty Life Liner', 3500, None, 30, 'best_seller'),
                ('Eva Foundation', 800, 650, 60, 'sale'),
                ('Pond\'s BB Cream', 400, None, 80, 'new'),
                ('Garnier BB Cream', 500, 400, 70, 'sale'),
                ('Nivea CC Cream', 450, None, 75, 'best_seller'),
                ('La Roche-Posay BB Cream', 2800, 2400, 35, 'featured'),
                ('The Ordinary Coverage Foundation', 2200, None, 40, 'new'),
                ('CeraVe BB Cream', 1800, 1500, 50, 'sale'),
            ],
        },
        'Lipstick': {
            'subcategories': ['Lipstick', 'Lip Gloss', 'Lip Balm', 'Lip Liner'],
            'products': [
                ('Huda Beauty Lipstick', 2800, None, 40, 'best_seller'),
                ('Eva Lipstick', 300, 240, 90, 'sale'),
                ('Pond\'s Lipstick', 250, None, 100, 'new'),
                ('Garnier Lip Balm', 200, 160, 120, 'sale'),
                ('Nivea Lip Balm', 150, None, 150, 'best_seller'),
                ('La Roche-Posay Lip Balm', 1200, 1000, 60, 'featured'),
                ('The Ordinary Lip Balm', 800, None, 70, 'new'),
                ('CeraVe Lip Balm', 600, 480, 80, 'sale'),
            ],
        },
        'Mascara': {
            'subcategories': ['Mascara', 'Eyeliner', 'Eyeshadow', 'Blush'],
            'products': [
                ('Huda Beauty Mascara', 2200, None, 35, 'best_seller'),
                ('Eva Mascara', 250, 200, 80, 'sale'),
                ('Pond\'s Mascara', 200, None, 90, 'new'),
                ('Garnier Mascara', 300, 240, 75, 'sale'),
                ('Nivea Mascara', 350, None, 70, 'best_seller'),
                ('La Roche-Posay Mascara', 1800, 1500, 40, 'featured'),
                ('The Ordinary Mascara', 1200, None, 50, 'new'),
                ('CeraVe Mascara', 1400, 1200, 45, 'sale'),
            ],
        },
    },
    'wellness': {
        'Essential Oils': {
            'subcategories': ['Essential Oils', 'Face Masks', 'Body Scrub', 'Sunscreen'],
            'products': [
                ('The Ordinary 100% Plant-Derived Squalane', 2400, None, 40, 'best_seller'),
                ('Himalaya Essential Oil', 600, 480, 60, 'sale'),
                ('Eva Essential Oil', 400, None, 70, 'new'),
                ('Pond\'s Essential Oil', 350, 280, 80, 'sale'),
                ('Nivea Essential Oil', 450, None, 65, 'best_seller'),
                ('La Roche-Posay Essential Oil', 3200, 2800, 30, 'featured'),
                ('Garnier Essential Oil', 550, None, 75, 'new'),
                ('CeraVe Essential Oil', 2200, 1800, 45, 'sale'),
            ],
        },
        'Face Masks': {
            'subcategories': ['Face Masks', 'Sheet Masks', 'Clay Masks', 'Sleeping Masks'],
            'products': [
                ('Himalaya Face Mask', 300, None, 100, 'best_seller'),
                ('Eva Face Mask', 200, 160, 120, 'sale'),
                ('Pond\'s Face Mask', 150, None, 140, 'new'),
                ('Garnier Face Mask', 250, 200, 90, 'sale'),
                ('Nivea Face Mask', 180, None, 110, 'best_seller'),
                ('La Roche-Posay Face Mask', 1500, 1300, 50, 'featured'),
                ('The Ordinary Face Mask', 1200, None, 60, 'new'),
                ('CeraVe Face Mask', 1000, 800, 70, 'sale'),
            ],
        },
        'Sunscreen': {
            'subcategories': ['Sunscreen', 'After Sun', 'Sunblock', 'SPF Cream'],
            'products': [
                ('CeraVe Sunscreen SPF 50', 2800, None, 50, 'best_seller'),
                ('La Roche-Posay Sunscreen', 3500, 3000, 40, 'featured'),
                ('Garnier Sunscreen', 600, 480, 80, 'sale'),
                ('Nivea Sunscreen', 450, None, 70, 'new'),
                ('Eva Sunscreen', 400, 320, 85, 'sale'),
                ('Pond\'s Sunscreen', 350, None, 90, 'best_seller'),
                ('Himalaya Sunscreen', 500, 400, 75, 'new'),
                ('The Ordinary Sunscreen', 2200, 1800, 45, 'sale'),
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def download_image(url, dest_dir, filename, stdout=None):
    """
    Download an image from `url` and save it to media/<dest_dir>/<filename>.
    Returns the relative media path (e.g. 'products/prod_xyz.jpg').
    Falls back to copying a static placeholder if the download fails.
    """
    abs_dir = os.path.join(settings.MEDIA_ROOT, dest_dir)
    os.makedirs(abs_dir, exist_ok=True)
    dest_path = os.path.join(abs_dir, filename)
    rel_path  = os.path.join(dest_dir, filename)

    if os.path.exists(dest_path):
        return rel_path  # already downloaded

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(dest_path, 'wb') as f:
                f.write(resp.read())
        if stdout:
            stdout.write(f'      ↓ downloaded {filename}')
        time.sleep(0.3)   # be polite to Unsplash
        return rel_path
    except Exception as exc:
        if stdout:
            stdout.write(f'      ⚠ download failed ({exc}), using placeholder')
        return _use_placeholder(dest_dir, filename)


def _use_placeholder(dest_dir, filename):
    """Copy a local static image as a placeholder."""
    static_img = os.path.join(settings.BASE_DIR, 'static', 'images', 'product-item-1.jpg')
    abs_dir    = os.path.join(settings.MEDIA_ROOT, dest_dir)
    os.makedirs(abs_dir, exist_ok=True)
    dest = os.path.join(abs_dir, filename)
    if os.path.exists(static_img) and not os.path.exists(dest):
        shutil.copy2(static_img, dest)
    return os.path.join(dest_dir, filename)


def safe_filename(name):
    return name[:40].replace(' ', '_').replace('/', '_').replace("'", '').replace('"', '')


def get_sizes(category_type, subcat_name):
    return SKINCARE_SIZES


# ---------------------------------------------------------------------------
# Management command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = 'Seed database with Pakistani clothing data and real product images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete all existing products, categories and subcategories before seeding',
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write(self.style.WARNING('Flushing existing data...'))
            Product.objects.all().delete()
            SubCategory.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write('  Done.\n')

        variant_count = 0
        product_count = 0
        fallback_idx  = 0

        for category_type, categories in SEED.items():
            self.stdout.write(self.style.HTTP_INFO(f'\n── {category_type.upper()} ──'))

            for cat_name, data in categories.items():
                # ── Category image ────────────────────────────────────────
                cat_img_url  = CAT_IMAGES.get(category_type, FALLBACK_POOL[0])
                cat_img_file = f'cat_{category_type}_{safe_filename(cat_name)}.jpg'
                cat_img_path = download_image(
                    cat_img_url, 'categories', cat_img_file, self.stdout
                )

                cat, created = Category.objects.get_or_create(
                    name=cat_name, category_type=category_type,
                    defaults={
                        'description': f'GlowCare {cat_name} for {category_type} care',
                        'image': cat_img_path,
                    }
                )
                if not created and not cat.image:
                    cat.image = cat_img_path
                    cat.save()

                self.stdout.write(f'  {"+" if created else "~"} Category: {cat}')

                # ── SubCategories ─────────────────────────────────────────
                for sub_name in data['subcategories']:
                    sub_key      = sub_name.lower()
                    sub_img_url  = SUBCAT_IMAGES.get(sub_key, SUBCAT_IMAGES['default'])
                    sub_img_file = f'sub_{safe_filename(sub_name)}.jpg'
                    sub_img_path = download_image(
                        sub_img_url, 'subcategories', sub_img_file, self.stdout
                    )

                    sub, _ = SubCategory.objects.get_or_create(
                        category=cat, name=sub_name,
                        defaults={'image': sub_img_path}
                    )
                    if not sub.image:
                        sub.image = sub_img_path
                        sub.save()

                # ── Products — distribute evenly across subcategories ─────
                subcats = list(cat.subcategories.all())
                if not subcats:
                    continue

                for i, (pname, price, disc, _stock, tag) in enumerate(data['products']):
                    if Product.objects.filter(name=pname).exists():
                        self.stdout.write(f'    ~ skipped (exists): {pname}')
                        continue

                    # Pick image URL
                    prod_img_url  = PRODUCT_IMAGES.get(
                        pname.lower(),
                        FALLBACK_POOL[fallback_idx % len(FALLBACK_POOL)]
                    )
                    fallback_idx += 1
                    prod_img_file = f'prod_{safe_filename(pname)}.jpg'
                    prod_img_path = download_image(
                        prod_img_url, 'products', prod_img_file, self.stdout
                    )

                    assigned_sub = subcats[i % len(subcats)]
                    product = Product.objects.create(
                        subcategory=assigned_sub,
                        name=pname,
                        description=DESCRIPTIONS[i % len(DESCRIPTIONS)],
                        price=price,
                        discount_price=disc,
                        stock=0,          # stock managed via variants
                        image=prod_img_path,
                        tag=tag,
                        is_active=True,
                    )
                    product_count += 1

                    # ── Variants ──────────────────────────────────────────
                    sizes = get_sizes(category_type, assigned_sub.name)
                    for size in sizes:
                        ProductVariant.objects.create(
                            product=product,
                            size=size,
                            stock=STOCK_MAP.get(size, 10),
                        )
                        variant_count += 1

                    self.stdout.write(
                        f'    + {product.name}  (Rs. {price:,}'
                        + (f' → Rs. {disc:,}' if disc else '')
                        + f')  [{tag or "no tag"}]'
                    )

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Seeded {product_count} products and {variant_count} variants.'
        ))
        self.stdout.write(
            'Note: Images downloaded from Unsplash (free licence). '
            'Run with --flush to reset and re-seed.'
        )

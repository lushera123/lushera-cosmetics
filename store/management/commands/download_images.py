"""
Downloads proper Pakistani/matching images from Unsplash for every
category, subcategory, product, and static banner/site image.

Usage:
    python manage.py download_images
    python manage.py download_images --force   # re-download even if file exists
"""
import os, time, urllib.request, urllib.error
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Category, SubCategory, Product

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# Unsplash photo IDs — carefully chosen to match Pakistani clothing context
# Format: https://images.unsplash.com/photo-<ID>?w=800&q=85&fit=crop
# ---------------------------------------------------------------------------

# ── CATEGORY hero images ────────────────────────────────────────────────────
CATEGORY_IMAGES = {
    # Pakistani man in shalwar kameez
    "men-shalwar kameez": "1594938298603-c8148c4b4e5b",
    # Pakistani man casual bottoms
    "men-bottoms":        "1507003211169-0a1dd7228f2d",
    # Men footwear / shoes
    "men-footwear":       "1542291026-7eec264c27ff",
    # Pakistani woman in lawn suit
    "women-lawn suits":   "1610030469983-98e550d6193c",
    # Pakistani woman formal wear
    "women-formal wear":  "1583391733956-3750e0ff4e8b",
    # Women heels / footwear
    "women-footwear":     "1543163521-1bf539c55dd2",
    # Pakistani boy in kurta
    "kids-boys":          "1622290291468-a28f7a7dc6a8",
    # Pakistani girl in frock
    "kids-girls":         "1518831959646-742c3a14ebf7",
    # Kids shoes
    "kids-footwear":      "1542291026-7eec264c27ff",
}

# ── SUBCATEGORY images ──────────────────────────────────────────────────────
SUBCATEGORY_IMAGES = {
    # Men
    "shalwar kameez":   "1594938298603-c8148c4b4e5b",
    "kurta":            "1598300042247-d088f8ab3a91",
    "sherwani":         "1617627143750-d86bc21e42bb",
    "waistcoat":        "1507679799987-c73779587ccf",
    "shalwar":          "1594938298603-c8148c4b4e5b",
    "trousers":         "1473966968600-fa801b869a1a",
    "jeans":            "1542272604-787c3835535d",
    "shorts":           "1591195853828-11db59a44f43",
    "khussay":          "1603808033192-082d6919d3e1",
    "chappal":          "1603487742131-4160ec999306",
    "sneakers":         "1542291026-7eec264c27ff",
    "sandals":          "1603487742131-4160ec999306",
    # Women
    "lawn suit":        "1610030469983-98e550d6193c",
    "embroidered suit": "1583391733956-3750e0ff4e8b",
    "casual kurti":     "1598300042247-d088f8ab3a91",
    "dupatta":          "1617627143750-d86bc21e42bb",
    "abaya":            "1559563458-527698bf5295",
    "gharara":          "1583391733956-3750e0ff4e8b",
    "lehenga":          "1583391733956-3750e0ff4e8b",
    # Kids
    "boys kurta":       "1622290291468-a28f7a7dc6a8",
    "t-shirts":         "1622290291468-a28f7a7dc6a8",
    "jackets":          "1622290291468-a28f7a7dc6a8",
    "girls frock":      "1518831959646-742c3a14ebf7",
    "leggings":         "1518831959646-742c3a14ebf7",
    "skirts":           "1518831959646-742c3a14ebf7",
    "school shoes":     "1542291026-7eec264c27ff",
}

# ── PRODUCT images ──────────────────────────────────────────────────────────
PRODUCT_IMAGES = {
    # Men Shalwar Kameez
    "white cotton shalwar kameez":  "1594938298603-c8148c4b4e5b",
    "blue linen shalwar kameez":    "1583391733956-3750e0ff4e8b",
    "embroidered eid kurta":        "1598300042247-d088f8ab3a91",
    "casual printed kurta":         "1598300042247-d088f8ab3a91",
    "classic black sherwani":       "1617627143750-d86bc21e42bb",
    "navy blue sherwani":           "1617627143750-d86bc21e42bb",
    "silk waistcoat":               "1507679799987-c73779587ccf",
    "embroidered waistcoat":        "1507679799987-c73779587ccf",
    # Men Bottoms
    "white cotton shalwar":         "1594938298603-c8148c4b4e5b",
    "slim fit shalwar":             "1594938298603-c8148c4b4e5b",
    "khaddar shalwar":              "1594938298603-c8148c4b4e5b",
    "pleated shalwar":              "1594938298603-c8148c4b4e5b",
    "formal trousers":              "1473966968600-fa801b869a1a",
    "slim fit jeans":               "1542272604-787c3835535d",
    "cargo shorts":                 "1591195853828-11db59a44f43",
    "jogger pants":                 "1473966968600-fa801b869a1a",
    # Men Footwear
    "leather khussay":              "1603808033192-082d6919d3e1",
    "embroidered khussay":          "1603808033192-082d6919d3e1",
    "casual chappal":               "1603487742131-4160ec999306",
    "formal leather sandal":        "1603487742131-4160ec999306",
    "white canvas sneakers":        "1542291026-7eec264c27ff",
    "running sneakers":             "1542291026-7eec264c27ff",
    "kolhapuri sandal":             "1603487742131-4160ec999306",
    "slip-on loafer":               "1542291026-7eec264c27ff",
    # Women Lawn Suits
    "printed lawn 3-piece suit":    "1610030469983-98e550d6193c",
    "embroidered lawn suit":        "1610030469983-98e550d6193c",
    "digital print lawn suit":      "1610030469983-98e550d6193c",
    "floral lawn 2-piece":          "1610030469983-98e550d6193c",
    "cotton kurti":                 "1598300042247-d088f8ab3a91",
    "printed kurti":                "1598300042247-d088f8ab3a91",
    "linen kurti":                  "1598300042247-d088f8ab3a91",
    "embroidered kurti":            "1598300042247-d088f8ab3a91",
    # Women Formal
    "bridal lehenga":               "1583391733956-3750e0ff4e8b",
    "party wear gharara":           "1583391733956-3750e0ff4e8b",
    "embroidered formal suit":      "1583391733956-3750e0ff4e8b",
    "velvet shawl suit":            "1583391733956-3750e0ff4e8b",
    "plain black abaya":            "1559563458-527698bf5295",
    "embroidered abaya":            "1559563458-527698bf5295",
    "open front abaya":             "1559563458-527698bf5295",
    "nida fabric abaya":            "1559563458-527698bf5295",
    # Women Footwear
    "embroidered khussa heels":     "1603808033192-082d6919d3e1",
    "bridal khussa":                "1603808033192-082d6919d3e1",
    "flat chappal":                 "1603487742131-4160ec999306",
    "block heel sandal":            "1543163521-1bf539c55dd2",
    "white sneakers":               "1542291026-7eec264c27ff",
    "platform sneakers":            "1542291026-7eec264c27ff",
    "kolhapuri flat":               "1603487742131-4160ec999306",
    "strappy heels":                "1543163521-1bf539c55dd2",
    # Kids Boys
    "boys cotton kurta":            "1622290291468-a28f7a7dc6a8",
    "boys eid kurta set":           "1622290291468-a28f7a7dc6a8",
    "boys printed t-shirt":         "1622290291468-a28f7a7dc6a8",
    "boys denim jeans":             "1622290291468-a28f7a7dc6a8",
    "boys cargo shorts":            "1622290291468-a28f7a7dc6a8",
    "boys hooded jacket":           "1622290291468-a28f7a7dc6a8",
    "boys jogger set":              "1622290291468-a28f7a7dc6a8",
    "boys graphic tee":             "1622290291468-a28f7a7dc6a8",
    # Kids Girls
    "girls floral frock":           "1518831959646-742c3a14ebf7",
    "girls embroidered frock":      "1518831959646-742c3a14ebf7",
    "girls lawn suit":              "1518831959646-742c3a14ebf7",
    "girls printed kurti":          "1518831959646-742c3a14ebf7",
    "girls leggings":               "1518831959646-742c3a14ebf7",
    "girls denim skirt":            "1518831959646-742c3a14ebf7",
    "girls party frock":            "1518831959646-742c3a14ebf7",
    "girls rainbow hoodie":         "1518831959646-742c3a14ebf7",
    # Kids Footwear
    "kids velcro sneakers":         "1542291026-7eec264c27ff",
    "kids school shoes":            "1542291026-7eec264c27ff",
    "kids sandals":                 "1603487742131-4160ec999306",
    "kids slip-on shoes":           "1542291026-7eec264c27ff",
    "kids canvas sneakers":         "1542291026-7eec264c27ff",
    "kids sport sandals":           "1603487742131-4160ec999306",
    "kids rain boots":              "1542291026-7eec264c27ff",
    "kids ankle boots":             "1542291026-7eec264c27ff",
}

# ── STATIC site images ──────────────────────────────────────────────────────
# (banner, category tiles, instagram grid, etc.)
# Each entry: (filename, unsplash_photo_id, width, height)
STATIC_IMAGES = [
    # Hero banners — Pakistani fashion scenes
    ("banner-image-1.jpg", "1594938298603-c8148c4b4e5b", 1400, 900),   # man shalwar kameez
    ("banner-image-2.jpg", "1610030469983-98e550d6193c", 1400, 900),   # woman lawn suit
    ("banner-image-3.jpg", "1583391733956-3750e0ff4e8b", 1400, 900),   # woman formal
    ("banner-image-4.jpg", "1622290291468-a28f7a7dc6a8", 1400, 900),   # kids
    ("banner-image-5.jpg", "1617627143750-d86bc21e42bb", 1400, 900),   # sherwani
    ("banner-image-6.jpg", "1598300042247-d088f8ab3a91", 1400, 900),   # kurti
    # Category tiles
    ("cat-item1.jpg",       "1594938298603-c8148c4b4e5b", 600, 750),   # men
    ("cat-item2.jpg",       "1610030469983-98e550d6193c", 600, 750),   # women
    ("cat-item3.jpg",       "1622290291468-a28f7a7dc6a8", 600, 750),   # kids
    ("cat-large-item1.jpg", "1617627143750-d86bc21e42bb", 800, 600),   # sherwani
    ("cat-large-item2.jpg", "1583391733956-3750e0ff4e8b", 800, 600),   # formal women
    ("cat-large-item3.jpg", "1598300042247-d088f8ab3a91", 800, 600),   # kurti
    ("cat-sm-item.jpg",     "1603808033192-082d6919d3e1", 400, 400),   # khussa
    ("cat-sm-item2.jpg",    "1603487742131-4160ec999306", 400, 400),   # chappal
    ("cat-sm-item3.jpg",    "1542291026-7eec264c27ff",   400, 400),   # sneakers
    # Collection / single image
    ("single-image-2.jpg",  "1583391733956-3750e0ff4e8b", 800, 1000),
    ("collection-banner.jpg","1610030469983-98e550d6193c", 1200, 600),
    # Newsletter / video bg
    ("bg-newsletter.jpg",   "1594938298603-c8148c4b4e5b", 1200, 500),
    ("video-image.jpg",     "1617627143750-d86bc21e42bb", 1400, 800),
    ("video-image-2.jpg",   "1583391733956-3750e0ff4e8b", 1400, 800),
    # Instagram grid — mix of Pakistani fashion
    ("insta-item1.jpg",     "1594938298603-c8148c4b4e5b", 500, 500),
    ("insta-item2.jpg",     "1610030469983-98e550d6193c", 500, 500),
    ("insta-item3.jpg",     "1598300042247-d088f8ab3a91", 500, 500),
    ("insta-item4.jpg",     "1617627143750-d86bc21e42bb", 500, 500),
    ("insta-item5.jpg",     "1583391733956-3750e0ff4e8b", 500, 500),
    ("insta-item6.jpg",     "1622290291468-a28f7a7dc6a8", 500, 500),
    # Product items (used as fallback)
    ("product-item-1.jpg",  "1594938298603-c8148c4b4e5b", 600, 750),
    ("product-item-2.jpg",  "1610030469983-98e550d6193c", 600, 750),
    ("product-item-3.jpg",  "1598300042247-d088f8ab3a91", 600, 750),
    ("product-item-4.jpg",  "1617627143750-d86bc21e42bb", 600, 750),
    ("product-item-5.jpg",  "1583391733956-3750e0ff4e8b", 600, 750),
    ("product-item-6.jpg",  "1622290291468-a28f7a7dc6a8", 600, 750),
    ("product-item-7.jpg",  "1603808033192-082d6919d3e1", 600, 750),
    ("product-item-8.jpg",  "1603487742131-4160ec999306", 600, 750),
    ("product-item-9.jpg",  "1542291026-7eec264c27ff",   600, 750),
    ("product-item-10.jpg", "1559563458-527698bf5295",   600, 750),
    # Wishlist items
    ("wishlist-item1.jpg",  "1610030469983-98e550d6193c", 500, 600),
    ("wishlist-item2.jpg",  "1598300042247-d088f8ab3a91", 500, 600),
    ("wishlist-item3.jpg",  "1583391733956-3750e0ff4e8b", 500, 600),
    # Newsletter image
    ("newsletter-image.jpg","1610030469983-98e550d6193c", 600, 400),
]


def fetch(url, dest, force=False, stdout=None):
    if os.path.exists(dest) and not force:
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            with open(dest, "wb") as f:
                f.write(r.read())
        time.sleep(0.25)
        return True
    except Exception as e:
        if stdout:
            stdout.write(f"  FAIL {os.path.basename(dest)}: {e}")
        return False


def unsplash_url(photo_id, w, h):
    return (
        f"https://images.unsplash.com/photo-{photo_id}"
        f"?w={w}&h={h}&fit=crop&crop=center&q=85&auto=format"
    )


class Command(BaseCommand):
    help = "Download Pakistani-context images from Unsplash for all DB records and static files"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true",
                            help="Re-download even if file already exists")

    def handle(self, *args, **options):
        force = options["force"]
        media = settings.MEDIA_ROOT
        static = settings.BASE_DIR / "static" / "images"
        ok = fail = 0

        # ── 1. Categories ────────────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO("\n── Categories ──"))
        for cat in Category.objects.all():
            key = f"{cat.category_type}-{cat.name.lower()}"
            pid = CATEGORY_IMAGES.get(key) or CATEGORY_IMAGES.get(f"{cat.category_type}-footwear")
            if not pid:
                continue
            dest = os.path.join(media, str(cat.image).replace("\\", "/"))
            url  = unsplash_url(pid, 800, 1000)
            if fetch(url, dest, force, self.stdout):
                self.stdout.write(f"  ✓ {cat}")
                ok += 1
            else:
                fail += 1

        # ── 2. SubCategories ─────────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO("\n── SubCategories ──"))
        for sub in SubCategory.objects.all():
            key = sub.name.lower()
            pid = SUBCATEGORY_IMAGES.get(key)
            if not pid:
                # fallback: use parent category key
                pkey = f"{sub.category.category_type}-{sub.category.name.lower()}"
                pid  = CATEGORY_IMAGES.get(pkey, "1594938298603-c8148c4b4e5b")
            dest = os.path.join(media, str(sub.image).replace("\\", "/"))
            url  = unsplash_url(pid, 600, 750)
            if fetch(url, dest, force, self.stdout):
                self.stdout.write(f"  ✓ {sub.name}")
                ok += 1
            else:
                fail += 1

        # ── 3. Products ──────────────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO("\n── Products ──"))
        for prod in Product.objects.all():
            key = prod.name.lower()
            pid = PRODUCT_IMAGES.get(key)
            if not pid:
                # fallback: subcategory key
                skey = prod.subcategory.name.lower()
                pid  = SUBCATEGORY_IMAGES.get(skey, "1594938298603-c8148c4b4e5b")
            dest = os.path.join(media, str(prod.image).replace("\\", "/"))
            url  = unsplash_url(pid, 800, 1000)
            if fetch(url, dest, force, self.stdout):
                self.stdout.write(f"  ✓ {prod.name}")
                ok += 1
            else:
                fail += 1

        # ── 4. Static site images ────────────────────────────────────────────
        self.stdout.write(self.style.HTTP_INFO("\n── Static images ──"))
        os.makedirs(static, exist_ok=True)
        for fname, pid, w, h in STATIC_IMAGES:
            dest = os.path.join(static, fname)
            url  = unsplash_url(pid, w, h)
            if fetch(url, dest, force, self.stdout):
                self.stdout.write(f"  ✓ {fname}")
                ok += 1
            else:
                fail += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone — {ok} downloaded, {fail} failed."
        ))

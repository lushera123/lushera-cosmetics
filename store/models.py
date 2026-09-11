from django.db import models
from django.utils.text import slugify


CATEGORY_CHOICES = [
    ('face', 'Face Care'),
    ('body', 'Body Care'),
    ('hair', 'Hair Care'),
    ('makeup', 'Makeup'),
    ('wellness', 'Wellness'),
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='face')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category_type}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_category_type_display()} - {self.name}"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'SubCategories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.slug}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} > {self.name}"


PRODUCT_TAG_CHOICES = [
    ('', 'None'),
    ('new', 'New Arrival'),
    ('sale', 'Sale'),
    ('best_seller', 'Best Seller'),
    ('featured', 'Featured'),
]


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    tag = models.CharField(max_length=20, choices=PRODUCT_TAG_CHOICES, blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def total_stock(self):
        """Total stock across all variants, falls back to legacy stock field."""
        variant_stock = sum(v.stock for v in self.variants.all())
        return variant_stock if self.variants.exists() else self.stock

    @property
    def is_in_stock(self):
        return self.total_stock > 0

    @property
    def available_sizes(self):
        return self.variants.filter(stock__gt=0).values_list('size', flat=True).distinct()

    @property
    def available_colors(self):
        return self.variants.filter(stock__gt=0).exclude(color='').values_list('color', flat=True).distinct()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"


SIZE_CHOICES = [
    ('30ml', '30 ml'), ('50ml', '50 ml'), ('100ml', '100 ml'),
    ('150ml', '150 ml'), ('200ml', '200 ml'), ('250ml', '250 ml'),
    ('500ml', '500 ml'), ('1L', '1 L'),
]

COLOR_CHOICES = [
    ('unscented', 'Unscented'), ('citrus', 'Citrus'), ('floral', 'Floral'),
    ('mint', 'Mint'), ('rose', 'Rose'), ('vanilla', 'Vanilla'),
    ('herbal', 'Herbal'), ('fruity', 'Fruity'),
]


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('product', 'size', 'color')
        ordering = ['size']

    @property
    def final_price(self):
        """Return discount price if available, otherwise regular price, fallback to product price."""
        if self.discount_price:
            return self.discount_price
        elif self.price:
            return self.price
        else:
            return self.product.final_price

    @property
    def display_price(self):
        """Return variant price if set, otherwise product price."""
        return self.price if self.price else self.product.price

    @property
    def display_discount_price(self):
        """Return variant discount price if set, otherwise product discount price."""
        return self.discount_price if self.discount_price else self.product.discount_price

    @property
    def is_in_stock(self):
        return self.stock > 0

    def __str__(self):
        parts = [self.product.name, self.size]
        if self.color:
            parts.append(self.color)
        return ' / '.join(parts)

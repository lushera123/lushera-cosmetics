"""
Seeds ProductVariant records for all existing skincare products.
Usage: python manage.py seed_variants
"""
from django.core.management.base import BaseCommand
from store.models import Product, ProductVariant

VOLUME_SIZES = ['30ml', '50ml', '100ml', '150ml', '200ml', '250ml', '500ml', '1L']

STOCK_MAP = {
    '30ml': 10, '50ml': 15, '100ml': 20, '150ml': 18,
    '200ml': 16, '250ml': 12, '500ml': 10, '1L': 8,
}


def get_sizes(product):
    return VOLUME_SIZES


class Command(BaseCommand):
    help = 'Seed variants for all products'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()
        created_count = 0
        for product in products:
            if product.variants.exists():
                continue
            sizes = get_sizes(product)
            for size in sizes:
                stock = STOCK_MAP.get(size, 10)
                ProductVariant.objects.create(
                    product=product,
                    size=size,
                    stock=stock,
                )
                created_count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Created {created_count} variants for {products.count()} products.'
        ))

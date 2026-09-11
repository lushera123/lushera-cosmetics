from django.db import models
from django.conf import settings
from store.models import Product


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, blank=True)

    @property
    def count(self):
        return self.products.count()

    def __str__(self):
        return f"Wishlist of {self.user.email}"

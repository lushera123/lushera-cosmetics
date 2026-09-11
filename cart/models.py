from django.db import models
from django.conf import settings
from store.models import Product, ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count()

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    

    class Meta:
        unique_together = ('cart', 'product', 'variant')

    @property
    def size(self):
        return self.variant.size if self.variant else ''

    @property
    def color(self):
        return self.variant.color if self.variant else ''

    @property
    def subtotal(self):
        return self.product.final_price * self.quantity

    def __str__(self):
        label = f"{self.quantity}x {self.product.name}"
        if self.variant:
            label += f" ({self.variant.size}"
            if self.variant.color:
                label += f" / {self.variant.color}"
            label += ")"
        return label

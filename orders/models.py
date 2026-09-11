from django.db import models
from django.conf import settings
from store.models import Product, ProductVariant


ORDER_STATUS = [
    ('pending',   'Pending'),
    ('confirmed', 'Confirmed'),
    ('processing','Processing'),
    ('shipped',   'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD_CHOICES = [
    ('cod',       'Cash on Delivery'),
    ('jazzcash',  'JazzCash'),
    ('easypaisa', 'EasyPaisa'),
]

PAYMENT_STATUS_CHOICES = [
    ('unpaid',  'Unpaid'),
    ('pending', 'Payment Pending'),
    ('paid',    'Paid'),
    ('failed',  'Failed'),
    ('refunded','Refunded'),
]

SHIPPING_COST = 200   # Rs. 200 flat; free above FREE_SHIPPING_THRESHOLD
FREE_SHIPPING_THRESHOLD = 3000


class Order(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status         = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')

    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    transaction_id = models.CharField(max_length=100, blank=True, help_text='JazzCash/EasyPaisa transaction ID')

    # Shipping
    full_name      = models.CharField(max_length=200)
    email          = models.EmailField()
    phone          = models.CharField(max_length=20)
    address        = models.TextField()
    city           = models.CharField(max_length=100)
    postal_code    = models.CharField(max_length=20)
    notes          = models.TextField(blank=True, help_text='Special instructions for delivery')

    # Amounts
    subtotal       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount   = models.DecimalField(max_digits=10, decimal_places=2)

    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True)
    courier         = models.CharField(max_length=100, blank=True, help_text='e.g. TCS, Leopards, M&P')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"

    @property
    def can_cancel(self):
        """User can cancel only if order hasn't shipped yet."""
        return self.status in ('pending', 'confirmed', 'processing')

    @property
    def status_steps(self):
        """Returns ordered list of (step_name, is_done, is_current) for timeline."""
        flow = ['pending', 'confirmed', 'processing', 'shipped', 'delivered']
        if self.status == 'cancelled':
            return [(s, False, False) for s in flow]
        try:
            current_idx = flow.index(self.status)
        except ValueError:
            current_idx = 0
        result = []
        for i, step in enumerate(flow):
            result.append((step, i < current_idx, i == current_idx))
        return result


class OrderItem(models.Model):
    order        = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product      = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant      = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    size         = models.CharField(max_length=20, blank=True)
    color        = models.CharField(max_length=20, blank=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    quantity     = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

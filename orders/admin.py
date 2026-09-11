from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'size', 'color', 'price', 'quantity', 'subtotal_display')
    fields = ('product_name', 'size', 'color', 'price', 'quantity', 'subtotal_display')
    can_delete = False

    def subtotal_display(self, obj):
        return f"Rs. {obj.subtotal:,.0f}"
    subtotal_display.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = (
        'id', 'user_email', 'full_name', 'status_badge', 'status', 'payment_method',
        'payment_status_badge', 'total_display', 'created_at'
    )
    list_filter   = ('status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('user__email', 'full_name', 'phone', 'transaction_id', 'tracking_number')
    readonly_fields = ('created_at', 'updated_at', 'subtotal', 'total_amount')
    list_editable = ('status',)
    ordering      = ('-created_at',)
    inlines       = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': ('user', 'status', 'created_at', 'updated_at')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'transaction_id')
        }),
        ('Shipping', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'postal_code', 'notes')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'courier')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'shipping_cost', 'total_amount')
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Customer'

    def total_display(self, obj):
        return f"Rs. {obj.total_amount:,.0f}"
    total_display.short_description = 'Total'

    def status_badge(self, obj):
        colors = {
            'pending':    '#f39c12',
            'confirmed':  '#3498db',
            'processing': '#9b59b6',
            'shipped':    '#1abc9c',
            'delivered':  '#d4af37',
            'cancelled':  '#e74c3c',
        }
        color = colors.get(obj.status, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;'
            'font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def payment_status_badge(self, obj):
        colors = {
            'unpaid':  '#f39c12',
            'pending': '#3498db',
            'paid':    '#d4af37',
            'failed':  '#e74c3c',
            'refunded':'#1abc9c',
        }
        color = colors.get(obj.payment_status, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;'
            'font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'

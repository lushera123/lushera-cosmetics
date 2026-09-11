from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from cart.models import Cart
from .models import Order, OrderItem, SHIPPING_COST, FREE_SHIPPING_THRESHOLD
from .forms import CheckoutForm


def send_order_emails(order):
    """Send order notification to admin and confirmation to customer."""
    try:
        # 1. Email to ADMIN
        admin_email = getattr(settings, 'ADMIN_EMAIL', '') or settings.EMAIL_HOST_USER
        if admin_email:
            admin_html = render_to_string('orders/email_new_order_admin.html', {'order': order})
            admin_msg = EmailMultiAlternatives(
                subject=f'🛍️ New Order #{order.id} — Rs. {int(order.total_amount)} — {order.shipping_name}',
                body=f'New order #{order.id} received from {order.shipping_name}. Total: Rs. {int(order.total_amount)}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            admin_msg.attach_alternative(admin_html, 'text/html')
            admin_msg.send(fail_silently=True)

        # 2. Confirmation email to CUSTOMER
        customer_email = order.user.email
        if customer_email:
            customer_html = render_to_string('orders/email_order_confirmation_customer.html', {'order': order})
            customer_msg = EmailMultiAlternatives(
                subject=f'✅ Order Confirmed #{order.id} — Lushera',
                body=f'Your order #{order.id} has been confirmed. Total: Rs. {int(order.total_amount)}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[customer_email],
            )
            customer_msg.attach_alternative(customer_html, 'text/html')
            customer_msg.send(fail_silently=True)

    except Exception as e:
        # Don't break the order flow if email fails
        print(f"Email error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Checkout
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart')

    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    # Shipping cost logic
    cart_subtotal = cart.total
    shipping = 0 if cart_subtotal >= FREE_SHIPPING_THRESHOLD else SHIPPING_COST
    grand_total = cart_subtotal + shipping

    # Get default address if exists
    default_address = request.user.addresses.filter(is_default=True).first()
    
    # Prepare initial data
    initial_data = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
    }
    
    # If default address exists, pre-fill from it
    if default_address:
        initial_data.update({
            'full_name': default_address.full_name,
            'phone': default_address.phone,
            'address': f"{default_address.address_line1}\n{default_address.address_line2}".strip(),
            'city': default_address.city,
            'postal_code': default_address.postal_code,
            'country': default_address.country,
        })
    else:
        # Fallback to user profile data
        initial_data.update({
            'phone': request.user.phone,
            'address': request.user.address,
        })

    form = CheckoutForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        payment_method = form.cleaned_data['payment_method']
        transaction_id = form.cleaned_data.get('transaction_id', '').strip()

        # Validate transaction ID for online payments
        if payment_method in ('jazzcash', 'easypaisa') and not transaction_id:
            form.add_error('transaction_id',
                'Please enter your transaction ID for JazzCash / EasyPaisa payment.')
        else:
            order = form.save(commit=False)
            order.user          = request.user
            order.subtotal      = cart_subtotal
            order.shipping_cost = shipping
            order.total_amount  = grand_total
            order.payment_status = 'paid' if payment_method in ('jazzcash', 'easypaisa') else 'unpaid'
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order        = order,
                    product      = item.product,
                    variant      = item.variant,
                    product_name = item.product.name,
                    price        = item.product.final_price,
                    quantity     = item.quantity,
                    size         = item.size,
                    color        = item.color,
                )
                # Deduct stock
                if item.variant:
                    item.variant.stock = max(0, item.variant.stock - item.quantity)
                    item.variant.save()
                else:
                    item.product.stock = max(0, item.product.stock - item.quantity)
                    item.product.save()

            cart.items.all().delete()
            # Send email notifications
            send_order_emails(order)
            messages.success(request, f'Order #{order.id} placed successfully! 🎉')
            return redirect('order_confirmation', order_id=order.id)

    # Get all user addresses for selection
    user_addresses = request.user.addresses.all()

    return render(request, 'orders/checkout.html', {
        'form':        form,
        'cart':        cart,
        'shipping':    shipping,
        'grand_total': grand_total,
        'free_threshold': FREE_SHIPPING_THRESHOLD,
        'user_addresses': user_addresses,
        'default_address': default_address,
    })


# ─────────────────────────────────────────────────────────────────────────────
# Order Confirmation (thank-you page)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})


# ─────────────────────────────────────────────────────────────────────────────
# Order List
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def order_list(request):
    orders = request.user.orders.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


# ─────────────────────────────────────────────────────────────────────────────
# Order Detail + Tracking
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


# ─────────────────────────────────────────────────────────────────────────────
# Cancel Order
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not order.can_cancel:
        messages.error(request, 'This order cannot be cancelled — it has already been shipped or delivered.')
        return redirect('order_detail', order_id=order.id)

    if request.method == 'POST':
        # Restore stock
        for item in order.items.all():
            if item.variant:
                item.variant.stock += item.quantity
                item.variant.save()
            elif item.product:
                item.product.stock += item.quantity
                item.product.save()

        order.status = 'cancelled'
        order.payment_status = 'refunded' if order.payment_status == 'paid' else order.payment_status
        order.save()
        messages.success(request, f'Order #{order.id} has been cancelled.')
        return redirect('order_list')

    return render(request, 'orders/cancel_order.html', {'order': order})


# ─────────────────────────────────────────────────────────────────────────────
# Invoice (printable)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def order_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})

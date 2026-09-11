from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from store.models import Product, ProductVariant
from .models import Cart, CartItem


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    cart_total = cart.total
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request.user)

    variant_id = request.POST.get('variant_id')
    variant = None

    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id, product=product)
        if not variant.is_in_stock:
            messages.error(request, f'Sorry, {product.name} ({variant.size}) is out of stock.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    elif product.variants.exists():
        # Variants exist but none selected — redirect back with message
        messages.warning(request, 'Please select a size before adding to cart.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, variant=variant
    )
    if not created:
        # Check stock before incrementing
        max_stock = variant.stock if variant else product.stock
        if item.quantity >= max_stock:
            messages.warning(request, f'Only {max_stock} available in stock.')
            return redirect(request.META.get('HTTP_REFERER', 'cart'))
        item.quantity += 1
        item.save()

    label = product.name
    if variant:
        label += f' ({variant.size}'
        if variant.color:
            label += f' / {variant.get_color_display()}'
        label += ')'
    messages.success(request, f'"{label}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    
    # Check if AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Return JSON for AJAX requests
    if is_ajax:
        cart = get_or_create_cart(request.user)
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': float(cart.total),
        })
    
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    
    # Check if AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if action == 'increase':
        max_stock = item.variant.stock if item.variant else item.product.stock
        if item.quantity < max_stock:
            item.quantity += 1
            item.save()
        else:
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': 'Maximum stock reached'
                })
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            cart = get_or_create_cart(request.user)
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'quantity': 0,
                    'subtotal': 0,
                    'cart_count': cart.item_count,
                    'cart_total': float(cart.total),
                })
            return redirect('cart')
    else:
        # Legacy support for quantity field
        qty = int(request.POST.get('quantity', 1))
        if qty > 0:
            max_stock = item.variant.stock if item.variant else item.product.stock
            item.quantity = min(qty, max_stock)
            item.save()
        else:
            item.delete()
    
    # Return JSON for AJAX requests
    if is_ajax:
        cart = get_or_create_cart(request.user)
        try:
            item.refresh_from_db()
            return JsonResponse({
                'success': True,
                'quantity': item.quantity,
                'subtotal': float(item.subtotal),
                'cart_count': cart.item_count,
                'cart_total': float(cart.total),
            })
        except CartItem.DoesNotExist:
            return JsonResponse({
                'success': True,
                'quantity': 0,
                'subtotal': 0,
                'cart_count': cart.item_count,
                'cart_total': float(cart.total),
            })
    
    return redirect('cart')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import Wishlist


def get_or_create_wishlist(user):
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    return wishlist


@login_required
def wishlist_view(request):
    wishlist = get_or_create_wishlist(request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_or_create_wishlist(request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        wishlist.products.add(product)
        messages.success(request, f'"{product.name}" added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))

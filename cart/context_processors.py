from .models import Cart


def cart_count(request):
    """Provides cart count, items, and total to all templates"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {
                'cart_count': cart.item_count,
                'cart_items_preview': cart.items.all()[:3],  # First 3 items for drawer
                'cart_total': cart.total,
            }
        except Cart.DoesNotExist:
            pass
    return {
        'cart_count': 0,
        'cart_items_preview': [],
        'cart_total': 0,
    }

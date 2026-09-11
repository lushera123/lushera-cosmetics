from .models import Wishlist


def wishlist_count(request):
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            return {'wishlist_count': wishlist.count}
        except Wishlist.DoesNotExist:
            pass
    return {'wishlist_count': 0}

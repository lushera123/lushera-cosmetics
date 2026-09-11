import json
import re
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from store.models import Product, Category


# ---------------------------------------------------------------------------
# Intent detection helpers
# ---------------------------------------------------------------------------

def _contains(text, *keywords):
    """Return True if any keyword appears as a word/phrase in text."""
    for kw in keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
            return True
    return False


def _extract_order_id(text):
    """Pull the first integer from text (e.g. 'order 42' → 42)."""
    m = re.search(r'\b(\d+)\b', text)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Response builders
# ---------------------------------------------------------------------------

def _order_status(user, text):
    if not user.is_authenticated:
        return (
            "Please <a href='/users/login/'>log in</a> first so I can look up your orders. 🔐"
        )

    order_id = _extract_order_id(text)

    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return f"I couldn't find Order #{order_id} linked to your account. Double-check the number?"

        status_emoji = {
            'pending':   '🕐',
            'confirmed': '✅',
            'shipped':   '🚚',
            'delivered': '📦',
            'cancelled': '❌',
        }.get(order.status, '📋')

        items_list = ', '.join(
            f"{i.product_name} ×{i.quantity}" for i in order.items.all()
        )
        return (
            f"{status_emoji} <strong>Order #{order.id}</strong><br>"
            f"Status: <strong>{order.get_status_display()}</strong><br>"
            f"Items: {items_list}<br>"
            f"Total: <strong>Rs. {order.total_amount:,}</strong><br>"
            f"Placed on: {order.created_at.strftime('%d %b %Y')}"
        )

    # No ID given — list recent orders
    orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    if not orders.exists():
        return "You haven't placed any orders yet. <a href='/'>Start shopping!</a> 🛍️"

    lines = []
    for o in orders:
        emoji = {'pending':'🕐','confirmed':'✅','shipped':'🚚','delivered':'📦','cancelled':'❌'}.get(o.status,'📋')
        lines.append(
            f"{emoji} <strong>Order #{o.id}</strong> — {o.get_status_display()} "
            f"(Rs. {o.total_amount:,}) — {o.created_at.strftime('%d %b %Y')}"
        )
    return (
        "Here are your recent orders:<br><br>"
        + "<br>".join(lines)
        + "<br><br>Share an order number for more details."
    )


def _product_search(text):
    # Strip common filler words to get the search term
    query = re.sub(
        r'\b(do you have|show me|find|search|looking for|i want|any|got|tell me about|what about)\b',
        '', text, flags=re.IGNORECASE
    ).strip(' ?.,!')

    if len(query) < 2:
        return "What product are you looking for? Tell me the name or type (e.g. 'cleanser', 'moisturizer', 'serum')."

    products = Product.objects.filter(name__icontains=query, is_active=True)[:5]
    if not products.exists():
        # Try broader search on individual words
        words = [w for w in query.split() if len(w) > 2]
        for word in words:
            products = Product.objects.filter(name__icontains=word, is_active=True)[:5]
            if products.exists():
                break

    if not products.exists():
        return (
            f"I couldn't find anything matching <strong>'{query}'</strong>. "
            f"Try browsing our <a href='/search/'>full catalogue</a> or check "
            f"<a href='/shop/face/'>Face Care</a>, <a href='/shop/body/'>Body Care</a>, "
            f"or <a href='/shop/hair/'>Hair Care</a>."
        )

    lines = []
    for p in products:
        price_str = f"Rs. {p.final_price:,}"
        if p.discount_price:
            price_str = f"<s>Rs. {p.price:,}</s> <strong>Rs. {p.discount_price:,}</strong>"
        lines.append(
            f"• <a href='/product/{p.slug}/'>{p.name}</a> — {price_str}"
        )
    return (
        f"Here's what I found for <strong>'{query}'</strong>:<br><br>"
        + "<br>".join(lines)
        + f"<br><br><a href='/search/?q={query}'>See all results →</a>"
    )


def _shipping_info():
    return (
        "🚚 <strong>Shipping & Delivery</strong><br><br>"
        "• <strong>Standard delivery:</strong> 3–5 working days<br>"
        "• <strong>Express delivery:</strong> 1–2 working days (available in major cities)<br>"
        "• <strong>Free shipping</strong> on orders above Rs. 3,000<br>"
        "• We deliver across all of Pakistan 🇵🇰<br><br>"
        "Once your order ships you'll receive a tracking number via email."
    )


def _returns_info():
    return (
        "🔄 <strong>Returns & Exchanges</strong><br><br>"
        "• Easy returns within <strong>7 days</strong> of delivery<br>"
        "• Item must be unused, unwashed, and in original packaging<br>"
        "• Exchange for a different size or colour is free<br>"
        "• Refunds are processed within 5–7 business days<br><br>"
        "To start a return, go to <a href='/orders/my-orders/'>My Orders</a> "
        "or email us at <a href='mailto:contact@glowcare.com'>contact@glowcare.com</a>."
    )


def _sizing_info():
    return (
        "📏 <strong>Size Guide</strong><br><br>"
        "<strong>Clothing (XS–XXL):</strong><br>"
        "XS → Chest 32–34\" | S → 34–36\" | M → 36–38\"<br>"
        "L → 38–40\" | XL → 40–42\" | XXL → 42–44\"<br><br>"
        "<strong>Shalwar Kameez:</strong> S/M/L/XL/XXL — standard Pakistani sizing<br><br>"
        "<strong>Kids:</strong> 3–4Y / 5–6Y / 7–8Y / 9–10Y / 11–12Y<br><br>"
        "Still unsure? Drop us an email at "
        "<a href='mailto:contact@glowcare.com'>contact@glowcare.com</a> with your measurements."
    )


def _payment_info():
    return (
        "💳 <strong>Payment Methods</strong><br><br>"
        "• Cash on Delivery (COD) — available nationwide<br>"
        "• Visa / Mastercard (online)<br>"
        "• JazzCash & EasyPaisa<br>"
        "• Bank transfer<br><br>"
        "All online payments are secured with SSL encryption. 🔒"
    )


from django.conf import settings as django_settings

def _contact_info():
    email = getattr(django_settings, 'STORE_EMAIL', 'contact@glowcare.com')
    phone = getattr(django_settings, 'STORE_PHONE', '+92 300 1234567')
    return (
        f"📞 <strong>Contact Us</strong><br><br>"
        f"• Email: <a href='mailto:{email}'>{email}</a><br>"
        f"• Phone: <a href='tel:{phone}'>{phone}</a><br>"
        "• Hours: Mon–Sat, 9 AM – 6 PM (PKT)<br><br>"
        "Or chat with us right here — I'm available 24/7! 😊"
    )


def _cart_help(user):
    if not user.is_authenticated:
        return (
            "To manage your cart, please <a href='/users/login/'>log in</a> first. "
            "Once logged in, you can view your cart at <a href='/cart/'>Cart</a>."
        )
    return (
        "🛒 <strong>Cart Help</strong><br><br>"
        "• <a href='/cart/'>View your cart</a><br>"
        "• To add an item, open any product and select your size, then click <em>Add to Cart</em><br>"
        "• You can update quantities or remove items directly from the cart page<br>"
        "• Ready to buy? Head to <a href='/orders/checkout/'>Checkout</a>"
    )


def _wishlist_help(user):
    if not user.is_authenticated:
        return "Please <a href='/users/login/'>log in</a> to use your wishlist. 💛"
    return (
        "💛 <strong>Wishlist</strong><br><br>"
        "• <a href='/wishlist/'>View your wishlist</a><br>"
        "• Click the heart icon on any product to save it<br>"
        "• Move items from wishlist to cart whenever you're ready"
    )


def _categories_info():
    cats = Category.objects.values('category_type').distinct()
    types = [c['category_type'] for c in cats]
    links = ' | '.join(
        f"<a href='/shop/{t}/'>{t.replace('_', ' ').title()}</a>" for t in types
    )
    return (
        f"🛍️ We carry premium skincare for: {links}<br><br>"
        "Popular categories:<br>"
        "• <a href='/shop/face/'>Face Care</a><br>"
        "• <a href='/shop/body/'>Body Care</a><br>"
        "• <a href='/shop/hair/'>Hair Care</a><br>"
        "• <a href='/shop/makeup/'>Makeup</a><br><br>"
        "Use the search bar or browse by category to explore."
    )


def _greeting(user):
    name = user.username if user.is_authenticated else "there"
    return (
        f"Assalam-o-Alaikum, <strong>{name}</strong>! 👋<br><br>"
        "I'm GlowCare's support assistant. Here's how I can help:<br><br>"
        "🔍 <strong>Search products</strong> — just type a product name<br>"
        "📦 <strong>Track your order</strong> — say 'track order' or 'order 42'<br>"
        "🚚 <strong>Shipping info</strong> — ask about delivery<br>"
        "🔄 <strong>Returns</strong> — ask about returns or exchanges<br>"
        "📏 <strong>Size guide</strong> — ask about sizing<br>"
        "💳 <strong>Payment</strong> — ask about payment methods<br>"
        "📞 <strong>Contact us</strong> — ask for contact details<br><br>"
        "What can I help you with today?"
    )


# ---------------------------------------------------------------------------
# Main intent router
# ---------------------------------------------------------------------------

def get_bot_response(user, message):
    t = message.strip().lower()

    # Greetings
    if _contains(t, 'hi', 'hello', 'hey', 'salam', 'assalam', 'aoa', 'help', 'start'):
        return _greeting(user)

    # Order tracking
    if _contains(t, 'order', 'track', 'status', 'where is my', 'my order', 'orders'):
        return _order_status(user, t)

    # Shipping
    if _contains(t, 'shipping', 'delivery', 'deliver', 'ship', 'how long', 'days', 'dispatch'):
        return _shipping_info()

    # Returns
    if _contains(t, 'return', 'exchange', 'refund', 'send back', 'replace', 'policy', 'policies'):
        return _returns_info()

    # Sizing
    if _contains(t, 'size', 'sizing', 'fit', 'measurement', 'chart', 'small', 'large', 'medium'):
        return _sizing_info()

    # Payment
    if _contains(t, 'payment', 'pay', 'cod', 'cash', 'jazzcash', 'easypaisa', 'card', 'visa', 'mastercard'):
        return _payment_info()

    # Cart
    if _contains(t, 'cart', 'basket', 'add to cart', 'remove from cart'):
        return _cart_help(user)

    # Wishlist
    if _contains(t, 'wishlist', 'wish list', 'saved', 'favourite', 'favorite'):
        return _wishlist_help(user)

    # Contact
    if _contains(t, 'contact', 'email', 'phone', 'call', 'reach', 'support', 'whatsapp'):
        return _contact_info()

    # Categories / browsing
    if _contains(t, 'categor', 'browse', 'shop', 'collection', 'face', 'body', 'hair', 'makeup', 'wellness', 'what do you sell', 'products'):
        return _categories_info()

    # Fallback — try product search
    if len(t) >= 3:
        result = _product_search(t)
        # If the search found something, return it
        if "couldn't find" not in result:
            return result

    # Final fallback
    return (
        "I'm not sure I understood that. 🤔 Here are some things I can help with:<br><br>"
        "• Type a <strong>product name</strong> to search (e.g. 'cleanser', 'moisturizer', 'facial oil')<br>"
        "• Say <strong>'track order'</strong> or <strong>'order 42'</strong> to check status<br>"
        "• Ask about <strong>shipping</strong>, <strong>returns</strong>, <strong>sizing</strong>, or <strong>payment</strong><br>"
        "• Say <strong>'contact'</strong> to reach our team<br><br>"
        "Or email us at <a href='mailto:contact@glowcare.com'>contact@glowcare.com</a> 📧"
    )


# ---------------------------------------------------------------------------
# AJAX endpoint
# ---------------------------------------------------------------------------

@require_POST
@csrf_exempt
def chatbot_response(request):
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not message:
        return JsonResponse({'reply': 'Please type a message first. 😊'})

    if len(message) > 500:
        return JsonResponse({'reply': 'Message too long. Please keep it under 500 characters.'})

    reply = get_bot_response(request.user, message)
    return JsonResponse({'reply': reply})

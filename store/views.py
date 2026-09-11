from django.shortcuts import render, get_object_or_404
from .models import Category, SubCategory, Product


def home(request):
    # Get all category types with their categories
    all_categories = {}
    for cat_type, cat_display in [('makeup', 'Makeup'), ('face', 'Skincare'), ('hair', 'Haircare'), ('wellness', 'Wellness'), ('men', 'Men'), ('women', 'Women'), ('kids', 'Kids')]:
        cats = Category.objects.filter(category_type=cat_type)
        if cats.exists():
            all_categories[cat_type] = {
                'display': cat_display,
                'categories': cats
            }
    
    featured     = Product.objects.filter(is_active=True, tag='featured').order_by('-created_at')[:10]
    new_arrivals = Product.objects.filter(is_active=True, tag='new').order_by('-created_at')[:10]
    best_sellers = Product.objects.filter(is_active=True, tag='best_seller').order_by('?')[:10]
    sale_items   = Product.objects.filter(is_active=True, tag='sale').order_by('?')[:10]

    # fallbacks if tags not set yet
    if not new_arrivals.exists():
        new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:10]
    if not best_sellers.exists():
        best_sellers = Product.objects.filter(is_active=True, discount_price__isnull=False).order_by('?')[:10]
    if not featured.exists():
        featured = new_arrivals

    related_products = Product.objects.filter(is_active=True).order_by('?')[:10]

    return render(request, 'store/home.html', {
        'all_categories':  all_categories,
        'featured':        featured,
        'new_arrivals':    new_arrivals,
        'best_sellers':    best_sellers,
        'sale_items':      sale_items,
        'related_products': related_products,
    })


def category_list(request, category_type):
    categories = Category.objects.filter(category_type=category_type)
    category_display = categories.first().get_category_type_display() if categories.exists() else category_type.title()
    return render(request, 'store/category_list.html', {
        'categories': categories,
        'category_type': category_type,
        'category_display': category_display,
    })


def subcategory_list(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    subcategories = category.subcategories.all()
    return render(request, 'store/subcategory_list.html', {
        'category': category,
        'subcategories': subcategories,
    })


def product_list(request, subcat_slug):
    subcategory = get_object_or_404(SubCategory, slug=subcat_slug)
    products = subcategory.products.filter(is_active=True)

    # filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    return render(request, 'store/product_list.html', {
        'subcategory': subcategory,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        subcategory=product.subcategory, is_active=True
    ).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


def search(request):
    from django.template.loader import render_to_string
    from django.http import JsonResponse

    query    = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort      = request.GET.get('sort', 'newest')
    is_ajax   = request.GET.get('ajax') == '1'

    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(name__icontains=query)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    all_categories = Category.objects.all()

    if is_ajax:
        html = render_to_string(
            'store/partials/product_grid.html',
            {'products': products},
            request=request
        )
        return JsonResponse({'html': html, 'count': products.count()})

    return render(request, 'store/search.html', {
        'products': products,
        'query': query,
        'all_categories': all_categories,
    })


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:
            # Send email to admin
            from django.core.mail import send_mail
            from django.conf import settings
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', '') or settings.EMAIL_HOST_USER
                if admin_email:
                    send_mail(
                        subject=f'Contact Form: {subject} — from {name}',
                        message=f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[admin_email],
                        fail_silently=True,
                    )
            except Exception:
                pass
            from django.contrib import messages as msg
            msg.success(request, 'Your message has been sent! We will get back to you soon.')
            from django.shortcuts import redirect
            return redirect('contact')
        else:
            from django.contrib import messages as msg
            msg.error(request, 'Please fill in all required fields.')

    return render(request, 'store/contact.html')

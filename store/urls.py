from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('shop/<str:category_type>/', views.category_list, name='category_list'),
    path('category/<slug:cat_slug>/', views.subcategory_list, name='subcategory_list'),
    path('subcategory/<slug:subcat_slug>/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]

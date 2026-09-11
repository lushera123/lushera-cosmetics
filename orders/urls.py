from django.urls import path
from . import views

urlpatterns = [
    path('checkout/',                    views.checkout,           name='checkout'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/',                   views.order_list,         name='order_list'),
    path('<int:order_id>/',              views.order_detail,       name='order_detail'),
    path('<int:order_id>/cancel/',       views.cancel_order,       name='cancel_order'),
    path('<int:order_id>/invoice/',      views.order_invoice,      name='order_invoice'),
]

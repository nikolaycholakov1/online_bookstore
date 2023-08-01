# store/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/checkout/', views.checkout_view, name='checkout'),
]

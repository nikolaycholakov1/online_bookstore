# store/urls.py

from django.urls import path
from .views import AddToCartView, CartView, RemoveFromCartView, CheckoutView, OrderSummaryView, \
    ChangeCartItemQuantityView

urlpatterns = [
    path('add-to-cart/<int:pk>', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('change-cart-item-quantity/', ChangeCartItemQuantityView.as_view(), name='change-cart-item-quantity'),
]

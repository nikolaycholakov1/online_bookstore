# store/urls.py

# Django imports
from django.urls import path

# Local imports
from .views import (
    AddToCartView,
    CartView,
    RemoveFromCartView,
    CheckoutView,
    ChangeCartItemQuantityView,
)

urlpatterns = [
    # Cart related paths
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('change-cart-item-quantity/', ChangeCartItemQuantityView.as_view(), name='change-cart-item-quantity'),

    # Checkout related path
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]

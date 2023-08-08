# store/admin.py

from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'total_items']
    inlines = [CartItemInline]
    readonly_fields = ['total_price']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'book', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_date', 'status', 'total_price']
    list_filter = ['status', 'order_date', 'user']
    search_fields = ['user__username', 'user__email']
    inlines = [OrderItemInline]
    readonly_fields = ['total_price']
    ordering = ['-order_date']
    date_hierarchy = 'order_date'
    raw_id_fields = ['user']
    list_per_page = 15


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'price']
    raw_id_fields = ['order', 'book']
    list_per_page = 15

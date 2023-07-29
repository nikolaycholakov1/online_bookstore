# book/admin.py

from django.contrib import admin
from .models import Customer, Book, BookReview, Order, OrderItem, DeliveryAddress


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Add custom options for the Customer model in the admin interface
    list_display = ('username', 'name', 'email', 'age', 'delivery_address')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'name', 'email')
    ordering = ('username',)
    list_per_page = 10


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Add custom options for the Book model in the admin interface
    list_display = ('title', 'author', 'price', 'featured', 'category')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'author')
    ordering = ('title',)
    list_per_page = 10


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    # Add custom options for the BookReview model in the admin interface
    list_display = ('user', 'book', 'review_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'book__title')
    ordering = ('-created_at',)
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Add custom options for the Order model in the admin interface
    list_display = ('user', 'order_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)  # Using double underscores for related fields
    ordering = ('-order_date',)
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    # Add custom options for the OrderItem model in the admin interface
    list_display = ('order', 'book', 'quantity', 'price')
    list_filter = ('order__status',)
    search_fields = ('order__user__username', 'book__title')
    ordering = ('-order__order_date',)
    list_per_page = 10


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    # Add custom options for the DeliveryAddress model in the admin interface
    list_display = ('customer', 'order', 'city', 'address', 'zip_code')
    list_filter = ('customer__is_staff', 'order__status')
    search_fields = ('customer__username', 'order__user__username')
    ordering = ('-date_added',)
    list_per_page = 10

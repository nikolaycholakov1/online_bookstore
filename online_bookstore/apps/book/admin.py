# book/admin.py

from django.contrib import admin
from .models import Customer, Book, BookReview, DeliveryAddress


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'age', 'delivery_address', 'get_review_count')
    list_filter = ('is_staff', 'is_active', 'age')
    search_fields = ('username', 'name', 'email')
    ordering = ('username',)
    list_per_page = 10

    def get_review_count(self, obj):
        return obj.bookreview_set.count()

    # Changes the name of the column
    get_review_count.short_description = 'Number of Reviews'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'featured', 'category', 'get_review_count')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'author')
    ordering = ('title',)
    list_per_page = 10

    def get_review_count(self, obj):
        return obj.reviews.count()

    get_review_count.short_description = 'Number of Reviews'


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'review_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'book__title')
    ordering = ('-created_at',)
    list_per_page = 10


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'order_date', 'status')
#     list_filter = ('status',)
#     search_fields = ('user__username',)
#     ordering = ('-order_date',)
#     list_per_page = 10


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     # Add custom options for the OrderItem model in the admin interface
#     list_display = ('order', 'book', 'quantity', 'price')
#     list_filter = ('order__status',)
#     search_fields = ('order__user__username', 'book__title')
#     ordering = ('-order__order_date',)
#     list_per_page = 10


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'country', 'city', 'address', 'zip_code', 'shipping_method')
    # before store app
    # list_filter = ('customer__is_staff', 'order__status')
    list_filter = ('customer__is_staff',)
    search_fields = ('customer__username', 'order__user__username')
    ordering = ('-zip_code',)
    list_per_page = 10

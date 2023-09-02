# book/admin.py

from django.contrib import admin
from .models import Customer, Book, BookReview


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'age', 'delivery_address', 'get_review_count')
    list_filter = ('is_staff', 'is_active', 'age')
    search_fields = ('username', 'email')
    ordering = ('username',)
    list_per_page = 10

    def get_review_count(self, obj):
        return obj.bookreview_set.count()

    # Changes the name of the column
    get_review_count.short_description = 'Number of Reviews'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'pages', 'featured', 'category', 'get_review_count')
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

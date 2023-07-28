from django.contrib import admin

from online_bookstore.apps.book.models import Book, BookReview

admin.site.register(Book)
admin.site.register(BookReview)
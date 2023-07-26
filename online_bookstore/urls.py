# project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('online_bookstore.apps.book.urls')),
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_bookstore.apps.core.urls')),
    path('', include('online_bookstore.apps.book.urls')),
    path('', include('online_bookstore.apps.order.urls')),
]

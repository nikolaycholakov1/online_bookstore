# project/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_bookstore.apps.book.urls')),
    path('', include('online_bookstore.apps.store.urls')),
]

handler404 = 'online_bookstore.apps.book.views.bad_request'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

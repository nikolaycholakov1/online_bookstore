# project/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import path, include
from online_bookstore.apps.book.views import Custom404View

handler404 = Custom404View.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_bookstore.apps.book.urls')),
    path('', include('online_bookstore.apps.store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# send_mail(
#     subject='Registration successful',
#     message='Hello',
#     from_email='greetings@emporium.com',
#     recipient_list=('nikolaycholakovdemo@gmail.com', )
# )
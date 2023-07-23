from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, HomePageView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', HomePageView.as_view(), name='home-page'),
    # Add other URL patterns for your project's views
]

# Add static and media URL configurations (if needed) for development environment
# This should not be used in production; for production, static and media files should be served by the web server or CDN.

#
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

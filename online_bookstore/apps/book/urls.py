# book/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, HomePageView, BookDetailView, profile_page, ProcessOrderView, publish_book

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home-page'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_page, name='profile-page'),

    path('book_detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('process_order/<int:pk>/', ProcessOrderView.as_view(), name='process_order'),
    path('publish/', publish_book, name='publish-book'),
]

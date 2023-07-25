from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from online_bookstore.apps.book.views import RegisterView, HomePageView, BookDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home-page'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('book_detail/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
]

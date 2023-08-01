# book/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, HomePageView, BookDetailView, ProcessOrderView, \
    CataloguePageView, EditBookView, PublishBookView, DeleteBookView, DeleteReviewView, ProfilePageView, LoginUserView, \
    LogoutUserView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),

    # path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home-page'), name='logout'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfilePageView.as_view(), name='profile-page'),

    path('publish/', PublishBookView.as_view(), name='publish-book'),
    path('catalogue/', CataloguePageView.as_view(), name='catalogue-page'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('process-order/<int:pk>/', ProcessOrderView.as_view(), name='process-order'),
    path('delete-book/<int:pk>/', DeleteBookView.as_view(), name='delete-book'),
    path('edit-book/<int:pk>/', EditBookView.as_view(), name='edit-book'),
    path('delete-review/<int:pk>/', DeleteReviewView.as_view(), name='delete-review'),

]

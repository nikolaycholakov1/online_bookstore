# book/urls.py
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path
from .views import (
    RegisterView, HomePageView, BookDetailView, CataloguePageView,
    EditBookView, PublishBookView, DeleteBookView, ProfilePageView,
    LoginUserView, LogoutUserView, MyOrdersView, EditReviewView,
    AboutUsView, CustomPasswordChangeView, UserListView, UserOrdersUpdateView, DeleteOrderView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),

    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('profile/', ProfilePageView.as_view(), name='profile-page'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/',
         PasswordChangeDoneView.as_view(template_name='registration/password-change-done.html'),
         name='password-change-done'),

    path('profile/my-orders/', MyOrdersView.as_view(), name='my-orders'),

    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('catalogue/', CataloguePageView.as_view(), name='catalogue-page'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('edit-review/<int:review_id>/', EditReviewView.as_view(), name='edit-review'),

    # For Staff only
    path('publish/', PublishBookView.as_view(), name='publish-book'),
    path('delete-book/<int:pk>/', DeleteBookView.as_view(), name='delete-book'),
    path('edit-book/<int:pk>/', EditBookView.as_view(), name='edit-book'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:username>/orders/', UserOrdersUpdateView.as_view(), name='user-orders-update'),
    path('order/delete/<int:pk>/', DeleteOrderView.as_view(), name='order-delete'),
]

# book/views.py
# Django core
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView
)
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    DeleteView, ListView, TemplateView, UpdateView
)
# Local imports
from .custom_mixins import AnonymousRequiredMixin, CustomPermissionDeniedMixin
from .forms import (
    BookPublishForm, CustomPasswordChangeForm,
    OrderUpdateForm, RegistrationForm, ReviewForm, UserProfileForm
)
from .models import Book, BookReview, Customer
from ..store.models import Order


# Reviewed
class RegisterView(AnonymousRequiredMixin, View):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home-page')

    def get(self, request):
        form = RegistrationForm()

        context = {
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Authenticate the user and log them in
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            return redirect(self.success_url)

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


# Reviewed
class LoginUserView(AnonymousRequiredMixin, LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        # Add a custom error message to the form
        form.add_error(None, "Incorrect username or password. Please try again.")
        return super().form_invalid(form)


# Reviewed
class LogoutUserView(LogoutView):
    next_page = 'home-page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Reviewed
class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

    def get(self, request, *args, **kwargs):
        # Fetch featured books from the database
        featured_books = Book.objects.filter(featured=True)

        context = {
            'featured_books': featured_books
        }

        return render(request, self.template_name, context)


# Reviewed
class ProfilePageView(CustomPermissionDeniedMixin, LoginRequiredMixin, View):
    NO_ACCESS_ERROR_MSG = 'Please log in to view this page.'
    SUCCESS_MESSAGE = 'Your profile has been updated successfully.'

    def get(self, request):
        user = request.user
        total_comments = user.get_total_comments()
        form = UserProfileForm(instance=user)

        context = {
            'form': form,
            'total_comments': total_comments,
        }

        return render(request, 'common/profile.html', context)

    def post(self, request):
        user = request.user
        total_comments = user.get_total_comments()
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, self.SUCCESS_MESSAGE)
        else:
            # Pass cleaned_data to the context to display in case of an invalid form submission
            context = {
                'form': form,
                'total_comments': total_comments,
                'cleaned_data': form.cleaned_data,
            }
            return render(request, 'common/profile.html', context)

        context = {
            'form': form,
            'total_comments': total_comments,
        }

        return render(request, 'common/profile.html', context)


# Reviewed
class CustomPasswordChangeView(CustomPermissionDeniedMixin, PasswordChangeView):
    template_name = 'registration/password-change-page.html'  # Name of your template
    success_url = reverse_lazy('password-change-done')
    form_class = CustomPasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context here if needed
        return context


# Reviewed
class AboutUsView(TemplateView):
    template_name = 'common/about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_members = Customer.objects.filter(is_staff=True)
        superusers = Customer.objects.filter(is_superuser=True)
        context['staff_members'] = staff_members
        context['superusers'] = superusers
        return context


# Reviewed
class MyOrdersView(CustomPermissionDeniedMixin, LoginRequiredMixin, View):
    NO_ACCESS_ERROR_MSG = 'Please log in to view this page.'

    template_name = 'common/my-orders.html'

    def get(self, request):
        # Retrieving the order information related to the current user
        orders = Order.objects.filter(user=request.user)

        context = {
            'orders': orders
        }
        return render(request, self.template_name, context)


# Reviewed but queryset method needs studying
class CataloguePageView(ListView):
    model = Book
    template_name = 'common/catalogue-page.html'
    context_object_name = 'books'
    paginate_by = 16

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            # Use Q objects to perform case-insensitive search on author, title, and category
            queryset = queryset.filter(
                Q(author__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(category__icontains=search_query)
            )

        return queryset.order_by('-price')


# 9

# Reviewed
class BookDetailView(View):
    template_name = 'books/book-detail.html'

    def get_book_and_reviews(self, pk):  # Utility method for fetching books and reviews
        book = get_object_or_404(Book, pk=pk)
        reviews = book.reviews.order_by('-created_at')
        return book, reviews

    def get(self, request, pk):
        book, reviews = self.get_book_and_reviews(pk)
        review_form = ReviewForm()

        context = {
            'book': book,
            'reviews': reviews,
            'review_form': review_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        book, reviews = self.get_book_and_reviews(pk)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book-detail', pk=pk)

        context = {
            'book': book,
            'reviews': reviews,
            'review_form': review_form,
        }

        return render(request, self.template_name, context)


# Reviewed Visit again
class EditReviewView(LoginRequiredMixin, UpdateView):
    template_name = 'books/edit-review.html'
    model = BookReview
    form_class = ReviewForm

    def get_success_url(self):
        review = self.object
        kwargs = {
            'pk': review.book.pk
        }
        return reverse_lazy('book-detail', kwargs=kwargs)

    def get_object(self, queryset=None):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(BookReview, id=review_id, user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['review_id'] = self.kwargs.get('review_id')
        return kwargs


# Book not found
# class BookNotFoundView(View):
#     template_name = 'error_pages/book-not-found.html'
#
#     def get(self, request, book_id):
#         book = get_object_or_404(Book, id=book_id)
#         return render(request, self.template_name, {'book': book})


# Reviewed
class PublishBookView(CustomPermissionDeniedMixin, LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'for_staff/publish-book.html'
    form_class = BookPublishForm
    NO_ACCESS_ERROR_MSG = 'You need staff privileges to publish a book.'

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        form = self.form_class()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home-page')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


# Reviewed
class DeleteBookView(CustomPermissionDeniedMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'for_staff/confirm-delete.html'
    model = Book
    success_url = reverse_lazy('catalogue-page')
    NO_ACCESS_ERROR_MSG = 'You need staff privileges to delete a book.'

    def test_func(self):
        return self.request.user.is_staff


# Reviewed
class EditBookView(CustomPermissionDeniedMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'for_staff/edit-book.html'
    model = Book
    form_class = BookPublishForm
    NO_ACCESS_ERROR_MSG = 'You need staff privileges to edit a book.'

    def get_success_url(self):
        kwargs = {
            'pk': self.object.pk
        }
        return reverse_lazy('book-detail', kwargs)

    def test_func(self):
        return self.request.user.is_staff


# Reviewed
class UserListView(CustomPermissionDeniedMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'for_staff/user-list.html'
    model = Customer
    context_object_name = 'users'
    NO_ACCESS_ERROR_MSG = 'You are not allowed to view this page.'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            total_orders=Count('orders', distinct=True),
            total_reviews=Count('bookreview', distinct=True)
        )

        return queryset.order_by('username')


# Reviewed
class UserOrdersUpdateView(CustomPermissionDeniedMixin, LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'for_staff/user-orders-update.html'
    NO_ACCESS_ERROR_MSG = 'You are not allowed to view this page.'

    def test_func(self):
        return self.request.user.is_staff

    def get_user(self, username):
        return get_object_or_404(Customer, username=username)

    def get(self, request, username):
        user = self.get_user(username)
        orders = Order.objects.filter(user=user)
        form = OrderUpdateForm()

        context = {
            'orders': orders,
            'customer': user,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, username):
        user = self.get_user(username)
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('user-orders-update', username=user.username)


# Reviewed
class DeleteOrderView(DeleteView):
    model = Order

    def get_success_url(self):
        order = self.object
        kwargs = {
            'username': order.user.username
        }

        return reverse_lazy('user-orders-update', kwargs=kwargs)


# Reviewed - only works with DEBUG=FALSE
class Custom404View(View):
    def get(self, request, exception):
        context = {}
        return render(request, 'error_pages/404.html', context, status=404)

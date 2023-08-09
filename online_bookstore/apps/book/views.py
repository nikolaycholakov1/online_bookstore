# book/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView

from .custom_mixins import AnonymousRequiredMixin
from .forms import RegistrationForm, ReviewForm, UserProfileForm, BookPublishForm, CustomPasswordChangeForm, \
    OrderUpdateForm
from .models import Book, BookReview, Customer
from ..store.models import Order


# Reviewed
class RegisterView(AnonymousRequiredMixin, View):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home-page')  # Use reverse_lazy to avoid import errors

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

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


# Reviewed
class ProfilePageView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        error_message = 'Please log in to view this page.'

        context = {
            'error_message': error_message
        }
        return render(self.request, 'error_pages/no-access.html', context)

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
            messages.success(request, 'Your profile has been updated successfully.')
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
class CustomPasswordChangeView(PasswordChangeView):
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
class MyOrdersView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        error_message = 'Please log in to view this page.'

        context = {
            'error_message': error_message
        }
        return render(self.request, 'error_pages/no-access.html', context)

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
        return reverse_lazy('book-detail', kwargs)

    def get_object(self, queryset=None):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(BookReview, id=review_id, user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['review_id'] = self.kwargs.get('review_id')
        return kwargs


# class BookNotFoundView(View):
#     template_name = 'error_pages/book-not-found.html'
#
#     def get(self, request, book_id):
#         book = get_object_or_404(Book, id=book_id)
#         return render(request, self.template_name, {'book': book})


# Reviewed
class PublishBookView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'books/publish-book.html'
    form_class = BookPublishForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        error_message = 'You need staff privileges to publish a book.'
        context = {
            'error_message': error_message
        }
        return render(self.request, 'error_pages/no-access.html', context)

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
class DeleteBookView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'books/confirm-delete.html'
    model = Book
    success_url = reverse_lazy('catalogue-page')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        error_message = 'You need staff privileges to delete a book.'
        context = {
            'error_message': error_message
        }
        return render(self.request, 'error_pages/no-access.html', context)


# Reviewed
class EditBookView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'books/edit-book.html'
    model = Book
    form_class = BookPublishForm

    def get_success_url(self):
        kwargs = {
            'pk': self.object.pk
        }
        return reverse_lazy('book-detail', kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        error_message = 'You need staff privileges to edit a book.'
        context = {
            'error_message': error_message
        }
        return render(self.request, 'error_pages/no-access.html', context)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Customer
    template_name = 'for_staff/user-list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_staff


class UserOrdersUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'for_staff/user-orders-update.html'

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, user_id):
        user = get_object_or_404(Customer, id=user_id)
        orders = Order.objects.filter(user=user)
        form = OrderUpdateForm()

        context = {
            'orders': orders,
            'customer': user,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, user_id):
        order = get_object_or_404(Order, id=request.POST.get('order_id'))
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('user-orders-update', user_id=user_id)


# Reviewed - only works with DEBUG=FALSE
class Custom404View(View):
    def get(self, request, exception):
        context = {}
        return render(request, 'error_pages/404.html', context, status=404)

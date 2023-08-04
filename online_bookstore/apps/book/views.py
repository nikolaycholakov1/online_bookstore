# book/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from .forms import RegistrationForm, ReviewForm, UserProfileForm, BookPublishForm
from .models import Book, BookReview
from ..store.models import Order


class ProfilePageView(LoginRequiredMixin, View):

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


class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch featured books from the database
        featured_books = Book.objects.filter(featured=True)
        context['featured_books'] = featured_books

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class MyOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        # Retrieving the order information related to the current user
        orders = Order.objects.filter(user=request.user)

        context = {
            'orders': orders
        }
        return render(request, 'common/my-orders.html', context)


class LoginUserView(LoginView):
    template_name = 'common/login.html'

    def form_invalid(self, form):
        # Add a custom error message to the form
        form.add_error(None, "Incorrect username or password. Please try again.")
        return super().form_invalid(form)


class LogoutUserView(LogoutView):
    next_page = 'home-page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegisterView(View):
    template_name = 'common/register.html'
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

            # Get the username and password from the form
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

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_number = self.request.GET.get('page')
        paginator = context['paginator']
        try:
            books = paginator.get_page(page_number)
        except PageNotAnInteger:
            books = paginator.get_page(1)
        except EmptyPage:
            books = paginator.get_page(paginator.num_pages)

        context = {
            'books': books,
            'is_paginated': books.has_other_pages(),
            'page_obj': books,
        }

        return context


class BookDetailView(View):
    template_name = 'books/book-detail.html'

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return redirect(reverse('book-not-found'))  # Redirect /book-not-found/

        reviews = book.reviews.order_by('-created_at')  # Sort reviews by date in descending order
        review_form = ReviewForm()

        context = {
            'book': book,
            'reviews': reviews,
            'review_form': review_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book-detail', pk=pk)

        reviews = book.reviews.order_by('-created_at')
        context = {
            'book': book,
            'reviews': reviews,
            'review_form': review_form,
        }

        return render(request, self.template_name, context)


class EditReviewView(LoginRequiredMixin, UpdateView):
    model = BookReview
    form_class = ReviewForm
    template_name = 'books/edit-review.html'

    def get_success_url(self):
        review = self.object
        return reverse_lazy('book-detail', kwargs={'pk': review.book.pk})

    def get_object(self, queryset=None):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(BookReview, id=review_id, user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['review_id'] = self.kwargs.get('review_id')
        return kwargs


class BookNotFoundView(View):
    template_name = 'error_pages/book-not-found.html'

    def get(self, request):
        return render(request, self.template_name)


class PublishBookView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'books/publish-book.html'
    form_class = BookPublishForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        # Redirect non-staff users to a different page with an error message
        return render(self.request, 'no-access.html')

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


class DeleteBookView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/confirm-delete.html'
    success_url = reverse_lazy('catalogue-page')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return render(self.request, 'no-access.html')


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        review = get_object_or_404(BookReview, pk=self.kwargs['pk'])
        if self.request.user.is_staff:
            review.delete()
            return redirect('book-detail', pk=review.book.pk)


# /TODO: Fix render no access
class EditBookView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookPublishForm
    template_name = 'books/edit_book.html'

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return render(self.request, 'no-access.html')


def bad_request(request, exception):
    context = {}
    return render(request, 'error_pages/404.html', context, status=400)

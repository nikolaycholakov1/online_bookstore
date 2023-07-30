# book/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView
from .forms import RegistrationForm, ReviewForm, ShippingInfoForm, UserProfileForm, BookPublishForm, OrderForm
from .models import Book, Order, OrderItem, DeliveryAddress, BookReview


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


class RegisterView(View):
    template_name = 'common/register.html'

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

            return redirect(reverse('home-page'))

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


class ProcessOrderView(View):

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return render(request, 'error404.html', {'message': 'Book not found'})

        shipping_info_form = ShippingInfoForm()

        context = {
            'book': book,
            'shipping_info_form': shipping_info_form,
        }
        return render(request, 'books/order-form.html', context)

    def post(self, request, pk):
        form = OrderForm(request.POST)

        if form.is_valid():

            try:
                book = Book.objects.get(pk=pk)
            except Book.DoesNotExist:
                return render(request, 'error404.html', {'message': 'Book not found'})

            quantity = form.cleaned_data['quantity']
            delivery_address = form.cleaned_data['delivery_address']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']

            order = Order.objects.create(user=request.user)

            OrderItem.objects.create(order=order, book=book, quantity=quantity, price=book.price)

            # Using request.user directly instead of request.user.customer
            DeliveryAddress.objects.create(
                customer=request.user,
                order=order,
                address=delivery_address,
                city=city,
                zip_code=zip_code
            )

            return redirect('home-page')

        context = {
            'form': form,
        }

        return render(request, 'common/home-page.html', context)


class PublishBookView(LoginRequiredMixin, View):
    template_name = 'books/publish-book.html'
    form_class = BookPublishForm

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


class BookDetailView(View):
    template_name = 'books/book-detail.html'

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        reviews = book.reviews.all()
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
            return redirect('book-detail', pk=pk)  # Redirect to the same book detail page

        reviews = book.reviews.all()
        context = {
            'book': book,
            'reviews': reviews,
            'review_form': review_form,
        }

        return render(request, self.template_name, context)


class DeleteBookView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/confirm-delete.html'
    success_url = reverse_lazy('catalogue-page')

    def test_func(self):
        return self.request.user.is_staff


class DeleteReviewView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        review = get_object_or_404(BookReview, pk=self.kwargs['pk'])
        if self.request.user.is_staff:
            review.delete()
            return redirect('book-detail', pk=review.book.pk)


class EditBookView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookPublishForm
    template_name = 'books/edit_book.html'

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.is_staff


# TODO: fix 404 page
def error_404_view(request, exception):
    return render(request, 'error404.html', status=404)

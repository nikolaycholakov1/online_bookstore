# book/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from .forms import RegistrationForm, ReviewForm, OrderForm, ShippingInfoForm, UserProfileForm
from .models import Book, Order, OrderItem, DeliveryAddress

from django.shortcuts import render
from .forms import UserProfileForm


@login_required
def profile_page(request):
    user = request.user  # Get the current logged-in user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'common/profile.html', {'form': form})


class BookDetailView(View):
    template_name = 'books/book_detail.html'

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
            return redirect('book_detail', pk=pk)  # Redirect to the same book detail page

        reviews = book.reviews.all()
        context = {
            'book': book,
            'reviews': reviews,
            'review_form': review_form,
        }

        return render(request, self.template_name, context)


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


class ProcessOrderView(View):

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return render(request, 'error.html', {'message': 'Book not found'})

        shipping_info_form = ShippingInfoForm()

        context = {
            'book': book,
            'shipping_info_form': shipping_info_form,
        }
        return render(request, 'books/order_form.html', context)

    def post(self, request, pk):  # Do not remove pk param or the Place Order button breaks
        form = OrderForm(request.POST)

        if form.is_valid():
            pk = form.cleaned_data['pk']

            try:
                book = Book.objects.get(pk=pk)
            except Book.DoesNotExist:
                return render(request, 'error.html', {'message': 'Book not found'})

            quantity = form.cleaned_data['quantity']
            delivery_address = form.cleaned_data['delivery_address']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']

            total_price = book.price * quantity

            order = Order.objects.create(user=request.user)

            OrderItem.objects.create(order=order, book=book, quantity=quantity, price=book.price)

            # Using request.user directly instead of request.user.customer
            DeliveryAddress.objects.create(customer=request.user, order=order,
                                           address=delivery_address, city=city, zip_code=zip_code)

            return redirect('home-page')

        context = {
            'form': form,
        }

        return render(request, 'books/order_form.html', context)

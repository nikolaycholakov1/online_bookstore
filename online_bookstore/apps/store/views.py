# store/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from ..book.models import Book


class AddToCartView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        quantity = int(request.POST.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.price = book.price if book.price else 0  # Set the price based on the book's price
        cart_item.save()

        return redirect('cart')


class CartView(View):
    def get(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()
        total_price = cart.total_price()

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price
        }

        return render(request, 'store/cart.html', context)


class RemoveFromCartView(View):
    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')

        try:
            cart_item = CartItem.objects.get(pk=cart_item_id, cart__user=request.user)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

        return redirect('cart')


class CheckoutView(View):
    def get(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()
        total_price = cart.total_price()
        form = CheckoutForm()

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price,
            'form': form
        }

        return render(request, 'store/checkout.html', context)

    def post(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # Process the form data and create the order
            # You need to implement this part based on your form fields and order creation logic
            # For simplicity, we assume the form contains shipping and payment information

            # Create the order
            order = Order.objects.create(user=request.user, status='Pending')

            # Move cart items to order items
            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(order=order, book=cart_item.book, quantity=cart_item.quantity,
                                         price=cart_item.price)

            # Clear the cart
            cart.cartitem_set.all().delete()

            return redirect('order_summary')  # Redirect to the order summary page or order confirmation page
        else:
            cart_items = cart.cartitem_set.all()
            total_price = cart.total_price()

            context = {
                'cart': cart,
                'cart_items': cart_items,
                'total_price': total_price,
                'form': form
            }

            return render(request, 'store/checkout.html', context)


class OrderSummaryView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        context = {
            'orders': orders
        }

        return render(request, 'store/order-summary.html', context)

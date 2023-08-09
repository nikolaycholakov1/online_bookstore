# store/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from ..book.models import Book


# Reviewed
class AddToCartView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        quantity = int(request.POST.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Try to retrieve an existing cart item for the book, or create a new one.
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.price = book.price
        cart_item.save()

        return redirect('cart')


# Reviewed but needs revisit to study
class CartView(LoginRequiredMixin, View):
    template_name = 'store/cart.html'
    login_url = 'login'

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_items = cart.cartitem_set.all()
        total_price = cart.total_price()

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total_price': total_price
        }

        return render(request, self.template_name, context)


# Reviewed
class RemoveFromCartView(View):
    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')

        cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user=request.user)
        cart_item.delete()

        return redirect('cart')


# Reviewed - Change to "Thank you for your order?"
# class OrderSummaryView(LoginRequiredMixin, View):
#     template_name = 'common/my-orders.html'
#     login_url = 'login'
#
#     def get(self, request):
#         orders = Order.objects.filter(user=request.user)
#
#         context = {
#             'orders': orders
#         }
#
#         return render(request, self.template_name, context)


# Reviewed. Can be refactored
class CheckoutView(LoginRequiredMixin, View):
    template_name = 'store/checkout.html'
    login_url = 'login'

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

        return render(request, self.template_name, context)

    def post(self, request):
        cart = Cart.objects.get_or_create(user=request.user)[0]

        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = Order.objects.create(user=request.user, status='Pending')

            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    price=cart_item.price
                )

            cart.cartitem_set.all().delete()

            context = {
                'order': order,
            }

            return render(request, 'store/thank-you.html', context)  # Redirect to the thank-you page

        else:
            cart_items = cart.cartitem_set.all()
            total_price = cart.total_price()

            context = {
                'cart': cart,
                'cart_items': cart_items,
                'total_price': total_price,
                'form': form
            }

            return render(request, self.template_name, context)


# Reviewed. Validation is not required
class ChangeCartItemQuantityView(View):

    def post(self, request):

        # Retrieve the cart item ID and the quantity change from the POST request
        cart_item_id = request.POST.get('cart_item_id')
        quantity_change = int(request.POST.get('quantity_change', 0))

        cart_item = self.get_cart_item(cart_item_id)
        cart = cart_item.cart

        # Update the quantity of the cart item based on the provided change
        self.update_cart_item_quantity(cart_item, quantity_change)

        # Create a response context with details about the updated cart
        context = {
            'success': True,
            'new_quantity': cart_item.quantity if cart_item.pk else 0,
            # Check if cart item still exists (wasn't deleted)
            'total_items': cart.total_items(),
        }

        return JsonResponse(context)

    @staticmethod
    def get_cart_item(cart_item_id):
        """
        Retrieve a cart item based on its ID.
        Returns the cart item if found, otherwise returns None.
        """
        try:
            return CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return None

    @staticmethod
    def update_cart_item_quantity(cart_item, quantity_change):
        """
        Update the quantity of a cart item.
        If the new quantity is 0 or less, the cart item is deleted.
        Otherwise, the cart item is updated with the new quantity.
        """
        cart_item.quantity += quantity_change
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

# store/views.py
from django.http import JsonResponse
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
            cart_item.price = book.price
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


class OrderSummaryView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        context = {
            'orders': orders
        }

        return render(request, 'common/my-orders.html', context)


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
            order = Order.objects.create(user=request.user, status='Pending')

            for cart_item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    price=cart_item.price
                )

            cart.cartitem_set.all().delete()

            return redirect('order-summary')
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


class ChangeCartItemQuantityView(View):
    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')
        quantity_change = int(request.POST.get('quantity_change', 0))

        if not cart_item_id or quantity_change == 0:
            context = {
                'success': False,
                'error': 'Invalid request'
            }
            return JsonResponse(context)

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            context = {
                'success': False,
                'error': 'Cart item not found'
            }
            return JsonResponse(context)

        # Update the cart item quantity and save the changes
        cart_item.quantity += quantity_change
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

        # Recalculate the cart's total price after the quantity changes
        cart = Cart.objects.get(user=request.user)
        total_price = cart.total_price()

        context = {
            'success': True,
            'new_quantity': cart_item.quantity,
            'total_items': cart.total_items(),
            'total_price': total_price,
        }

        return JsonResponse(context)

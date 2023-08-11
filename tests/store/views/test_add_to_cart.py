from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

from online_bookstore.apps.store.models import Book, Cart, CartItem
from online_bookstore.apps.store.views import AddToCartView


class AddToCartViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass123'
        )
        self.book = Book.objects.create(
            title="Sample Book",
            author="Sample Author",
            category="Fiction",
            description="A sample book description",
            pages=100,
            price=9.99,
        )

    def test_for_adding_book_to_cart(self):
        request = self.factory.post(reverse('add-to-cart', args=[self.book.pk]), {'quantity': 2})
        request.user = self.user

        response = AddToCartView.as_view()(request, pk=self.book.pk)

        # Verify the response redirects to the cart
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart'))

        # Verify the cart is created
        cart = Cart.objects.get(user=self.user)
        self.assertIsNotNone(cart)

        # Verify the book is added to cart with correct quantity
        cart_items = CartItem.objects.get(cart=cart, book=self.book)
        self.assertEqual(cart_items.quantity, 1)

    def test_for_increasing_quantity_of_existing_book_in_cart(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, book=self.book, quantity=1, price=self.book.price)

        request = self.factory.post(reverse('add-to-cart', args=[self.book.pk]), {'quantity': 3})
        request.user = self.user

        response = AddToCartView.as_view()(request, pk=self.book.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cart'))

        # Verify the book's quantity is updated in the cart
        cart_item = CartItem.objects.get(cart=cart, book=self.book)
        self.assertEqual(cart_item.quantity, 4)

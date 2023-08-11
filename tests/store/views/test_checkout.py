from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from online_bookstore.apps.book.models import Book
from online_bookstore.apps.store.models import Cart, CartItem, Order
from online_bookstore.apps.store.views import CheckoutView


class CheckoutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        self.book = Book.objects.create(
            title="Sample Book",
            category="Fiction",
            author="John Doe",
            description="Sample description",
            pages=100,
            price=10.99,
            cover_image='path/to/image.jpg'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            book=self.book,
            quantity=2,
            price=self.book.price
        )

    def test_for_get_checkout_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('checkout'))

        # Check response code
        self.assertEqual(response.status_code, 200)

        self.assertIn('cart', response.context)
        self.assertIn('cart_items', response.context)
        self.assertIn('total_price', response.context)
        self.assertIn('form', response.context)

    def test_for_unsuccessful_post_checkout_view(self):

        request = self.factory.post(reverse('checkout'), data={})  # Empty data makes the form invalid
        request.user = self.user

        response = CheckoutView.as_view()(request)

        self.assertEqual(response.status_code, 200)

        # Ensure the cart is still filled
        self.assertTrue(CartItem.objects.filter(cart=self.cart).exists())

        # Ensure no order is created
        self.assertFalse(Order.objects.filter(user=self.user).exists())

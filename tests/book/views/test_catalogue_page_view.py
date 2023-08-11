from django.test import TestCase
from django.urls import reverse
from django.db.models import Q

from online_bookstore.apps.book.models import Book


class CataloguePageViewTestCase(TestCase):

    def test_for_books_search_using_query(self):
        search_query = "Sample search text"

        # Simulate a GET request with django's test client
        response = self.client.get(reverse('catalogue-page'), {'search_query': search_query})
        expected_books = Book.objects.filter(
            Q(author__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query)
        )

        self.assertEqual(list(response.context['books']), list(expected_books))

    def test_for_books_ordered_by_price_in_descending_order(self):
        response = self.client.get(reverse('catalogue-page'))
        expected_books = Book.objects.all().order_by('-price')

        self.assertEqual(list(response.context['books']), list(expected_books))

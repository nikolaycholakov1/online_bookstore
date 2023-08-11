from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from online_bookstore.apps.book.models import Book, BookReview
from online_bookstore.apps.book.views import BookDetailView


class GetBookAndReviewsTestCase(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Sample Book",
            author="Sample Author",
            category="Fiction",
            description="A sample book description",
            pages=100,
            price=9.99,
            cover_image='path/to/sample.jpg'
        )

        # Sample reviews for the book
        user = get_user_model().objects.create_user(username="testuser", password="testpass123")

        BookReview.objects.create(
            book=self.book,
            user=user,
            review_text="Great book!"
        )
        BookReview.objects.create(
            book=self.book,
            user=user,
            review_text="Enjoyed reading it."
        )

    def test_for_valid_book_and_its_reviews(self):
        book, reviews = BookDetailView.get_book_and_reviews(self.book.pk)
        all_book_reviews = [review.review_text for review in reviews]

        self.assertEqual(book, self.book)
        self.assertEqual(reviews.count(), 2)
        self.assertIn("Great book!", all_book_reviews)
        self.assertIn("Enjoyed reading it.", all_book_reviews)

    def test_for_non_existent_book_raises_404(self):
        response = self.client.get(reverse('book-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

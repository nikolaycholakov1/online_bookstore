from django.core.exceptions import ValidationError
from django.test import TestCase

from online_bookstore.apps.book.models import Book, Customer, BookReview


class BookReviewModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            category='Fiction',
            author='Author',
            description='Description',
            price=10.99,
            cover_image='cover.jpg',
        )
        self.user = Customer.objects.create(
            username='testuser',
            email='test@example.com',
            # Add other required fields for your Customer model
        )
        self.valid_review = BookReview(
            book=self.book,
            user=self.user,
            review_text='This is a valid review.',
        )

    def test_valid_review_creation(self):
        self.valid_review.full_clean()  # Should not raise ValidationError

    def test_invalid_blank_review_text(self):
        self.valid_review.review_text = ''
        with self.assertRaises(ValidationError):
            self.valid_review.full_clean()

    def test_review_ordering_by_created_at(self):
        review1 = BookReview.objects.create(
            book=self.book,
            user=self.user,
            review_text='Review 1',
        )
        review2 = BookReview.objects.create(
            book=self.book,
            user=self.user,
            review_text='Review 2',
        )
        review3 = BookReview.objects.create(
            book=self.book,
            user=self.user,
            review_text='Review 3',
        )

        reviews = self.book.reviews.all()  # Fetch the reviews in descending order of created_at
        self.assertEqual(reviews[0], review3)
        self.assertEqual(reviews[1], review2)
        self.assertEqual(reviews[2], review1)

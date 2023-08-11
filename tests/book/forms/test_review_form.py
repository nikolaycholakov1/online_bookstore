from django.test import TestCase
from online_bookstore.apps.book.forms import ReviewForm


class ReviewFormTestCase(TestCase):

    def test_for_valid_review_text_submission(self):
        form_data = {'review_text': 'This is a great book!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_for_empty_review_text_submission(self):
        form_data = {'review_text': ''}
        form = ReviewForm(data=form_data)
        expected_error_message = 'This field is required.'

        self.assertFalse(form.is_valid())
        self.assertIn('review_text', form.errors)
        self.assertEqual(form.errors['review_text'][0], expected_error_message)


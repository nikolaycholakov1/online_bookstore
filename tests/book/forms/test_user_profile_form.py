from django.test import TestCase

from online_bookstore.apps.book.forms import UserProfileForm
from online_bookstore.apps.book.models import Customer


class UserProfileFormTest(TestCase):

    def test_for_username_with_non_alpha_characters(self):
        expected_error_message = 'Username can only contain letters and whitespace.'
        form = UserProfileForm(data={'username': 'User123'})

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'][0], expected_error_message)

    def test_for_first_name_with_non_alpha_characters(self):
        expected_error_message = 'First name can only contain letters and whitespace.'
        form = UserProfileForm(data={'first_name': 'John123'})

        # Assert the form is not valid due to the non-alpha characters in the first_name
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertEqual(form.errors['first_name'][0], expected_error_message)

    def test_for_last_name_with_non_alpha_characters(self):
        expected_error_message = 'Last name can only contain letters and whitespace.'
        form = UserProfileForm(data={'last_name': 'Doe123'})

        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertEqual(form.errors['last_name'][0], expected_error_message)

    def test_for_delivery_address_length_out_of_bounds(self):
        too_short = 'A' * (Customer.DELIVERY_ADDRESS_MIN_LEN - 1)
        too_long = 'A' * (Customer.DELIVERY_ADDRESS_MAX_LEN + 1)

        expected_error_message_bounds = f'Delivery address must be between {Customer.DELIVERY_ADDRESS_MIN_LEN} and {Customer.DELIVERY_ADDRESS_MAX_LEN} characters long.'
        expected_error_message_too_long = f'Ensure this value has at most {Customer.DELIVERY_ADDRESS_MAX_LEN} characters (it has {Customer.DELIVERY_ADDRESS_MAX_LEN + 1}).'

        form1 = UserProfileForm(data={'delivery_address': too_short})
        form2 = UserProfileForm(data={'delivery_address': too_long})

        # Asserts for too short
        self.assertFalse(form1.is_valid())
        self.assertIn('delivery_address', form1.errors)
        self.assertEqual(form1.errors['delivery_address'][0], expected_error_message_bounds)

        # Asserts for too long
        self.assertFalse(form2.is_valid())
        self.assertIn('delivery_address', form2.errors)
        self.assertEqual(form2.errors['delivery_address'][0], expected_error_message_too_long)

    def test_for_valid_form(self):
        data = {
            'username': 'JohnDoe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'age': 25,
            'profile_picture': 'some_image.jpg',
            'delivery_address': '123 Some Street, City',
        }
        form = UserProfileForm(data=data)
        self.assertTrue(form.is_valid())

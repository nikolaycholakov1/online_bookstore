from django.contrib.auth.models import User
from django.test import TestCase, Client

from online_bookstore.apps.book.models import Customer


class ProfilePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = Customer.objects.create(user=self.user)

    def test_get_profile_page(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/profile/')  # Adjust the URL as per your project
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/profile.html')

    def test_post_valid_profile_update(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/profile/', {
            # Provide valid POST data for UserProfileForm
            # e.g., 'first_name': 'Updated First Name'
        }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/profile.html')
        self.assertContains(response, 'Your profile has been updated successfully.')

    def test_post_invalid_profile_update(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/profile/', {
            # Provide invalid POST data for UserProfileForm
            # e.g., 'first_name': ''
        }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/profile.html')
        self.assertContains(response, 'This field is required.')

    def test_post_valid_profile_update_cleaned_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/profile/', {
            # Provide valid POST data for UserProfileForm
            # e.g., 'first_name': 'Updated First Name'
        }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/profile.html')
        self.assertContains(response, 'Updated First Name')  # Assuming 'first_name' is a field in your UserProfileForm

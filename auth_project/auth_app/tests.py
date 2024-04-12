from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, UserDetails

class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.user_details_url = reverse('user-details')
        self.update_profile_url = reverse('update-profile', kwargs={'pk': 1})
        self.delete_user_url = reverse('delete-user', kwargs={'pk': 1})

        # Create a user for testing login and other operations
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            phone='1234567890'
        )

        # Log in the test user
        response = self.client.post(self.login_url, {'email': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_signup(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'phone': '9876543210',
            'password': 'test1234'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        response = self.client.post(self.login_url, {'email': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_details(self):
        data = {
            'age': 25,
            'date_of_birth': '1999-01-01',
            'profession': 'Engineer',
            'address': '123 Main St, Anytown',
            'hobby': 'Reading'
        }
        response = self.client.post(self.user_details_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserDetails.objects.filter(user=self.user).exists())

    def test_update_profile(self):
        # Create a UserDetails instance for the user
        user_details_data = {
            'age': 25,
            'date_of_birth': '1999-01-01',
            'profession': 'Engineer',
            'address': '123 Main St, Anytown',
            'hobby': 'Reading'
        }
        UserDetails.objects.create(user=self.user, **user_details_data)

        # Ensure self.user has an existing profile
        self.assertTrue(UserDetails.objects.filter(user=self.user).exists())

        updated_data = {
            'age': 30,
            'date_of_birth': '1994-01-01',
            'profession': 'Software Developer',
            'address': '456 Elm St, Othertown',
            'hobby': 'Gardening'
        }

        # Construct the update URL for the user profile
        update_profile_url = reverse('update-profile', kwargs={'pk': self.user.userdetails.pk})

        # Perform a PUT request to update the user profile
        response = self.client.put(update_profile_url, updated_data)

        # Check if the response status code matches the expected 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the user object from the database and assert updated fields
        self.user.refresh_from_db()
        self.assertEqual(self.user.userdetails.age, 30)
        self.assertEqual(self.user.userdetails.profession, 'Software Developer')


    def test_delete_user(self):
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email='test@example.com').exists())

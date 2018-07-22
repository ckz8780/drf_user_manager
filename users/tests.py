from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserTests(APITestCase):

    def setUp(self):
        self.test_admin_user = User.objects.create_superuser('testadminuser', 'test@example.com', 'testadminpassword')
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

    def test_setup_created_correct_test_users(self):
        """
        Confirm that we have both a regular user and an admin user to test with.
        """
        test_user = User.objects.get(username="testuser")
        test_admin_user = User.objects.get(username="testadminuser")

        self.assertIsInstance(test_user, User)
        self.assertIsInstance(test_admin_user, User)

        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)
        
        self.assertTrue(test_admin_user.is_active)
        self.assertTrue(test_admin_user.is_staff)
        self.assertTrue(test_admin_user.is_superuser)

    def test_create_user_anonymously(self):
        """
        Confirm that anyone can create a username via /api/v1/users/create/
        """
        url = reverse('create-user')
        data = {
            "username": "createduser",
            "first_name": "Created",
            "last_name": "User",
            "email": "created@example.com",
            "password": "regularUser!"
        }
        response = self.client.post(url, data, format='json')
        new_user = User.objects.get(username='createduser')
        ignore_response_fields = ['id', 'password']
        
        response_status = response.status_code

        self.assertEqual(response_status, status.HTTP_201_CREATED)
        self.assertIsInstance(new_user, User)

    def test_api_response_to_user_creation_matches_post_data(self):
        """
        Confirm that the API responds w/ the same fields it was told to create
        """
        url = reverse('create-user')
        data = {
            "username": "createduser",
            "first_name": "Created",
            "last_name": "User",
            "email": "created@example.com",
            "password": "regularUser!"
        }
        response = self.client.post(url, data, format='json')
        ignore_response_fields = ['id', 'password']

        for k, v in response.data.items():
            if k not in ignore_response_fields:
                self.assertEqual(v, data[k])

    def test_password_not_in_api_response(self):
        """
        Confirm that the API does not return the password in the response.
        """
        url = reverse('create-user')
        data = {
            "username": "createduser",
            "first_name": "Created",
            "last_name": "User",
            "email": "created@example.com",
            "password": "regularUser!"
        }
        response = self.client.post(url, data, format='json')

        self.assertNotIn('password', response.data.keys())


    def test_cannot_update_user_anonymously(self):
        """
        Confirm that we cannot update a user anonymously
        """
        url = reverse('update-user', args=[2]) # Try to update the test user (pk=2)
        data = {
            "username": "updated_test_user",
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated@example.com",
            "password": "totally_different_password!"
        }
        
        self.client.force_authenticate(user=None) # No authentication
        response = self.client.put(url, data, format='json')
        response_detail = response.data['detail']
        response_status = response.status_code

        self.assertEqual(response_status, status.HTTP_403_FORBIDDEN)
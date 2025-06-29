# from django.test import TestCase
# Django imports
from django.contrib.auth import get_user_model
from django.urls import reverse

# Django REST Framework imports
from rest_framework.test import APITestCase

from src.users.models import User


class UserRegistrationTest(APITestCase):
    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'email': 'email1@gmail.com',
            'password': 'passwordWW@205',
            'password_check': 'passwordWW@205'
        })
        self.assertEquals(response.status_code, 201)
        self.assertTrue(get_user_model().objects.filter(email='email1@gmail.com'))

    def test_login(self):
        User.objects.create_user(email='email@gmail.com', password='testPassword2')
        response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com',
            'password': 'testPassword2'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTrue('access_token' in response.data)
        self.assertTrue('refresh_token' in response.data)

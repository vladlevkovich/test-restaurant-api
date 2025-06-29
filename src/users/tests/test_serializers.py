# Django imports
from django.test import TestCase

# from src.users.serializers import UserRegisterSerializer
from src.users.serializers import UserRegisterSerializer


class UserSerializerTestCase(TestCase):
    def test_user_register_serializer(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'StrongPass123',
            'password_check': 'StrongPass123'
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))
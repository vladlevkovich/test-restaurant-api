from datetime import timedelta

# Django imports
from django.urls import reverse
from django.utils import timezone

# Django REST Framework imports
from rest_framework.test import APITestCase

from src.cart.models import Cart, CartItem
from src.menu.models import Dish
from src.orders.models import Order
from src.orders.serializers import OrderReadSerializer
from src.users.models import User


class OrderCreateTestCase(APITestCase):
    def test_create_order(self):
        user = User.objects.create_user(email='email@gmail.com', password='passwordTest2')

        dish_1 = Dish.objects.create(
            name='Борщ',
            description='Насичений буряковий суп з овочами.',
            price=50.00,
            photo='dish/borsch.jpg'
        )
        dish_2 = Dish.objects.create(
            name='Стейк',
            description='Соковитий стейк.',
            price=100.00,
            photo='dish/steak.jpg'
        )

        user_response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com',
            'password': 'passwordTest2'
        })
        access_token = user_response.data['access_token']

        cart, _ = Cart.objects.get_or_create(user=user)
        CartItem.objects.create(cart=cart, dish=dish_1, quantity=2)
        CartItem.objects.create(cart=cart, dish=dish_2, quantity=1)

        delivery_time = (timezone.now() + timedelta(minutes=31)).isoformat()

        response = self.client.post(
            reverse('order_create'),
            {'delivery_time': delivery_time},
            headers={'Authorization': f'Bearer {access_token}'}
        )

        self.assertEqual(response.status_code, 201)
        order = Order.objects.get(user=user)
        serializer_data = OrderReadSerializer(order).data
        self.assertEqual(response.data, serializer_data)

        # Перевіряємо, що CartItem видалені з кошика
        self.assertFalse(CartItem.objects.filter(cart=cart).exists())

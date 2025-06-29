from datetime import timedelta

# Django imports
from django.test import RequestFactory, TestCase
from django.utils import timezone

from src.cart.models import Cart, CartItem
from src.menu.models import Dish
from src.orders.models import Order, OrderItem
from src.orders.serializers import (
    OrderCreateSerializer,
    OrderItemReadSerializer,
    OrderReadSerializer,
)
from src.users.models import User


class OrderSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.dish = Dish.objects.create(
            name='Борщ',
            description='Смачний борщ',
            price=50.00,
            photo='dish/borsch.jpg'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, dish=self.dish, quantity=2)
        self.factory = RequestFactory()

    def test_order_create_serializer_valid(self):
        delivery_time = timezone.now() + timedelta(minutes=40)
        data = {'delivery_time': delivery_time}
        request = self.factory.post('/', data)
        request.user = self.user
        serializer = OrderCreateSerializer(
            data={'delivery_time': delivery_time},
            context={'request': request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.delivery_time, delivery_time)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().dish, self.dish)
        self.assertEqual(order.items.first().quantity, 2)

    def test_order_create_serializer_invalid_time(self):
        delivery_time = timezone.now() + timedelta(minutes=10)
        request = self.factory.post('/', {'delivery_time': delivery_time})
        request.user = self.user
        serializer = OrderCreateSerializer(
            data={'delivery_time': delivery_time},
            context={'request': request}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('delivery_time', serializer.errors)

    def test_order_read_serializer(self):
        order = Order.objects.create(user=self.user, delivery_time=timezone.now() + timedelta(minutes=40))
        order_item = OrderItem.objects.create(order=order, dish=self.dish, quantity=3)
        serializer = OrderReadSerializer(order)
        data = serializer.data
        self.assertEqual(data['id'], str(order.id))
        self.assertEqual(data['delivery_time'], order.delivery_time.isoformat().replace('+00:00', 'Z'))
        self.assertEqual(data['is_ready'], order.is_ready)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['dish']['id'], str(self.dish.id))
        self.assertEqual(data['items'][0]['quantity'], 3)

    def test_order_item_read_serializer(self):
        order = Order.objects.create(user=self.user, delivery_time=timezone.now() + timedelta(minutes=40))
        order_item = OrderItem.objects.create(order=order, dish=self.dish, quantity=5)
        serializer = OrderItemReadSerializer(order_item)
        data = serializer.data
        self.assertEqual(data['id'], str(order_item.id))
        self.assertEqual(data['dish']['id'], str(self.dish.id))
        self.assertEqual(data['quantity'], 5)

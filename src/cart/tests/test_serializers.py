# Django imports
from django.test import TestCase

from src.cart.models import Cart, CartItem
from src.cart.serializers import CartItemReadSerializer, CartSerializer
from src.menu.models import Dish
from src.users.models import User


class CartSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='cartuser@example.com', password='testpass123')
        self.dish = Dish.objects.create(
            name='Піца',
            description='З сиром',
            price=200.00,
            is_available=True,
            photo=None
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, dish=self.dish, quantity=3)

    def test_cart_item_read_serializer(self):
        serializer = CartItemReadSerializer(self.cart_item)
        data = serializer.data
        self.assertEqual(data['id'], str(self.cart_item.id))
        self.assertEqual(data['dish']['id'], str(self.dish.id))
        self.assertEqual(data['dish']['name'], self.dish.name)
        self.assertEqual(data['quantity'], 3)

    def test_cart_serializer(self):
        serializer = CartSerializer(self.cart)
        data = serializer.data
        self.assertEqual(data['id'], str(self.cart.id))
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['dish'], self.dish.id)  # CartSerializer використовує id
        self.assertEqual(data['items'][0]['quantity'], 3)
        self.assertEqual(float(data['total']), 600.0)





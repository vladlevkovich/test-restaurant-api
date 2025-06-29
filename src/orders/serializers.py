from datetime import timedelta
from typing import Any, Dict, cast

# Django imports
from django.db import transaction
from django.utils import timezone

# Django REST Framework imports
from rest_framework import serializers

from src.cart.models import Cart
from src.menu.serializers import DishSerializer
from src.users.models import User

from .models import Order, OrderItem


class OrderCreateSerializer(serializers.Serializer):
    """Приймає тільки delivery_time, все інше бере з кошика."""
    delivery_time = serializers.DateTimeField()

    def validate_delivery_time(self, value):
        if value < timezone.now() + timedelta(minutes=30):
            raise serializers.ValidationError('Delivery time must be at least 30 minutes.')
        return value

    @transaction.atomic
    def create(self, validated_data: Dict[str, Any]) -> Order:
        user = cast(User, self.context['request'].user)
        cart = Cart.objects.get(user=user)
        if not cart.items.exists():
            raise serializers.ValidationError('The cart is empty.')

        order = Order.objects.create(
            user=user,
            delivery_time=validated_data['delivery_time']
        )
        order_items = [
            OrderItem(order=order, dish=ci.dish, quantity=ci.quantity)
            for ci in cart.items.all()
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.items.all().delete()
        return order

class OrderItemReadSerializer(serializers.ModelSerializer[OrderItem]):
    """
    Серіалайзер для товарів які замовили
    """
    dish = DishSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'dish', 'quantity')

class OrderReadSerializer(serializers.ModelSerializer[Order]):
    """
    Перегляд замовлення
    """
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'delivery_time', 'items', 'is_ready')

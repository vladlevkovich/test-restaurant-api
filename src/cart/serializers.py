from decimal import Decimal

# Django REST Framework imports
from rest_framework import serializers

from src.menu.serializers import DishSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer[CartItem]):
    class Meta:
        model = CartItem
        fields = ('dish', 'quantity')

class CartItemReadSerializer(serializers.ModelSerializer[CartItem]):
    dish = DishSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'dish', 'quantity')

class CartSerializer(serializers.ModelSerializer[Cart]):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self, obj: Cart):
        return sum(i.dish.price * i.quantity for i in obj.items.all())

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total')

class CartItemWriteSerializer(serializers.ModelSerializer[CartItem]):
    # dish = DishSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ('dish', 'quantity')

# Django REST Framework imports
from rest_framework import serializers

from .models import Dish


class DishSerializer(serializers.ModelSerializer[Dish]):
    class Meta:
        model = Dish
        fields = ('id', 'name', 'description', 'price', 'photo')

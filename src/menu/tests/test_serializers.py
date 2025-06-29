# Django imports
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from src.menu.models import Dish
from src.menu.serializers import DishSerializer


class DishSerializerTest(TestCase):
    def test_dish_serializer_serialization(self):
        dish = Dish.objects.create(
            name='Салат Цезар',
            description='Смачний салат з куркою',
            price=120.50,
            is_available=True,
            photo=None
        )
        serializer = DishSerializer(dish)
        data = serializer.data
        self.assertEqual(data['name'], 'Салат Цезар')
        self.assertEqual(data['description'], 'Смачний салат з куркою')
        self.assertEqual(data['price'], '120.50')
        self.assertIsNone(data['photo'])
        self.assertEqual(data['id'], str(dish.id))

    def test_dish_serializer_deserialization(self):
        data = {
            'name': 'Борщ',
            'description': 'Традиційний український суп',
            'price': '80.00',
            'is_available': True
        }
        serializer = DishSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        dish = serializer.save()
        self.assertEqual(dish.name, data['name'])
        self.assertEqual(dish.description, data['description'])
        self.assertEqual(str(dish.price), data['price'])
        self.assertTrue(dish.is_available)

    def test_dish_serializer_with_photo(self):
        data = {
            'name': 'Вареники',
            'description': 'З картоплею',
            'price': '60.00',
            'is_available': True,
        }
        serializer = DishSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        dish = serializer.save()
        self.assertIsNotNone(dish.photo)


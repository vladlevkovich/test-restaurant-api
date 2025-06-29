# Django imports
from django.urls import reverse

# Django REST Framework imports
from rest_framework.test import APITestCase

from src.cart.models import Cart, CartItem
from src.cart.serializers import CartItemReadSerializer
from src.menu.models import Dish
from src.users.models import User


class CartTestCase(APITestCase):
    def test_create_cart(self):
        user = User.objects.create_user(email='email@gmail.com', password='passwordTest2')
        dish_1 = Dish.objects.create(name='Борщ',
                                     description='Насичений буряковий суп з овочами, сметаною та зеленню. Подається з пампушками з часником.',
                                     price=50)
        user_response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com',
            'password': 'passwordTest2'
        })
        access_token = user_response.data['access_token']
        response = self.client.post(reverse('cart'), {
            'dish': dish_1.id,
            'quantity': 2
        }, headers={'Authorization': f'Bearer {access_token}'})

        expected_data = {
            'dish': dish_1.id,
            'quantity': 2
        }
        self.assertEquals(expected_data, response.data)
        self.assertEquals(201, response.status_code)

    def test_get_cart(self):
        user = User.objects.create_user(email='email@gmail.com', password='passwordTest2')

        dish_1 = Dish.objects.create(
            name='Салат Цезар з Куркою',
            description='Свіжий салат з хрустким листям ромейн, курячою грудкою, сухариками та соусом Цезар.',
            price=100.00,
            photo='dish/borsch-pampushkas-2000x1200_mvvWNBj.jpg'
        )
        dish_2 = Dish.objects.create(
            name='Гречка з Грибами та Цибулею',
            description="Здоровий гарнір з гречки, смажених грибів і підсмаженої цибулі. Ідеально до м'яса чи овочів.",
            price=50.00,
            photo='media/dish/borsch-pampushkas-2000x1200_Uw2R7L7.jpg'
        )

        user_response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com',
            'password': 'passwordTest2'
        })
        access_token = user_response.data['access_token']

        cart, _ = Cart.objects.get_or_create(user=user)

        CartItem.objects.create(cart=cart, dish=dish_1, quantity=1)
        CartItem.objects.create(cart=cart, dish=dish_2, quantity=1)

        response = self.client.get(
            reverse('cart'),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        cart_items = CartItem.objects.filter(cart=cart)
        serializer_data = CartItemReadSerializer(cart_items, many=True, context={'request': response.wsgi_request}).data

        total = sum(float(item['dish']['price']) * item['quantity'] for item in serializer_data)

        expected_data = {
            'items': serializer_data,
            'total': total
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

    def test_update_dish_in_cart(self):
        user = User.objects.create_user(email='email@gmail.com', password='passwordTest2')

        dish_1 = Dish.objects.create(
            name='Салат Цезар з Куркою',
            description='Свіжий салат з хрустким листям ромейн, курячою грудкою, сухариками та соусом Цезар.',
            price=100.00,
            photo='dish/borsch-pampushkas-2000x1200_mvvWNBj.jpg'
        )

        user_response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com',
            'password': 'passwordTest2'
        })
        access_token = user_response.data['access_token']

        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item = CartItem.objects.create(cart=cart, dish=dish_1, quantity=1)
        response = self.client.put(
            reverse('cart_detail', kwargs={'pk': cart_item.id}),
            {
                'quantity': 4
            },
            headers={'Authorization': f'Bearer {access_token}'}
        )
        cart_item.refresh_from_db()
        serializer_data = CartItemReadSerializer(cart_item, context={'request': response.wsgi_request}).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(cart_item.quantity, 4)

    def test_remove_item_from_cart(self):
        user = User.objects.create_user(email='email@gmail.com', password='passwordTest2')

        dish_1 = Dish.objects.create(
            name='Салат Цезар з Куркою',
            description='Свіжий салат з хрустким листям ромейн, курячою грудкою, сухариками та соусом Цезар.',
            price=100.00,
            photo='dish/borsch-pampushkas-2000x1200_mvvWNBj.jpg'
        )

        user_response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com',
            'password': 'passwordTest2'
        })
        access_token = user_response.data['access_token']

        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item = CartItem.objects.create(cart=cart, dish=dish_1, quantity=1)
        response = self.client.delete(
            reverse('cart_detail', kwargs={'pk': cart_item.id}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        expected_data = {
            'message': 'Item removed'
        }
        self.assertEqual(expected_data, response.data)

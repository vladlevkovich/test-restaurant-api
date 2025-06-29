# Django imports
from django.urls import reverse

# Django REST Framework imports
from rest_framework.test import APITestCase

from src.menu.models import Dish
from src.menu.serializers import DishSerializer
from src.users.models import User


class MenuListTestCase(APITestCase):
    def test_get_list_menu(self):
        User.objects.create_user(email='email@gmail.com', password='passwordTest2')
        dish_1 = Dish.objects.create(name='Борщ', description='Насичений буряковий суп з овочами, сметаною та зеленню. Подається з пампушками з часником.', price=50)
        dish_2 = Dish.objects.create(name='	Стейк зі Свинини', description='Соковитий свинячий стейк, приготований на грилі з травами, подається з овочевим гарніром.', price=100)
        user_response = self.client.post(reverse('login'), {
            'email': 'email@gmail.com',
            'password': 'passwordTest2'
        })
        access_token = user_response.data['access_token']
        response = self.client.get(reverse('menu_list'), headers={'Authorization': f'Bearer {access_token}'})
        serializer_data = DishSerializer([dish_1, dish_2], many=True).data
        self.assertEquals(serializer_data, response.data)

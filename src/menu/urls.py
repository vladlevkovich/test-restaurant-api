# Django imports
from django.urls import path

from .views import DishListView

urlpatterns = [
    path('', DishListView.as_view(), name='menu_list'),
]


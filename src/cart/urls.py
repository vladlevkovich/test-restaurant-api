# Django imports
from django.urls import path

from .views import *

urlpatterns = [
    path('items/', CartItemListCreateView.as_view(), name='cart'),
    path('items/<uuid:pk>/', CartItemDetailView.as_view(), name='cart_detail')
]
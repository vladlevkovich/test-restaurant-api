# Django imports
from django.urls import path

from .views import *

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order_create'),
    path('order/<uuid:pk>/', OrderDetailView.as_view(), name='order_detail')
    # path('', OrderCreateView.as_view(), name='order_create')
]

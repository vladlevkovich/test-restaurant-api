from datetime import datetime, timedelta
import uuid

# Django imports
from django.conf import settings
from django.db import models
from django.utils import timezone

from src.menu.models import Dish


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    delivery_time = models.DateTimeField()
    is_ready = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)    # чи відправлено email
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.delivery_time < timezone.now() + timedelta(minutes=30):
            raise ValueError('Delivery time should be at least 30 minutes.')

    def __str__(self) -> str:
        return f'{self.id} - {self.user.email}'

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.dish.name}x{self.quantity}'
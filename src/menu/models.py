import uuid

# Django imports
from django.db import models


class Dish(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    photo = models.ImageField(blank=True, null=True, upload_to='media/dish/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name}'

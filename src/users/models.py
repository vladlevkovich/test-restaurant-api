import uuid

# Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    username = None     # type: ignore

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()   # type: ignore

    def __str__(self) -> str:
        return f'{self.email}'

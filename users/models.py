from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class PositionChoices(models.TextChoices):
        Personal = ("Personal",)  # 개인
        Business = ("Business",)  # 기업

    name = models.CharField(
        max_length=20,
        blank=False,
    )

    position = models.CharField(
        max_length=20, blank=False, choices=PositionChoices.choices
    )
    email = models.EmailField(
        max_length=50,
        blank=False,
    )
    password = models.CharField(
        max_length=10,
        blank=False,
    )
    
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


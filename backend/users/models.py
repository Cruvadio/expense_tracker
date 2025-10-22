from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, verbose_name='Биография')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
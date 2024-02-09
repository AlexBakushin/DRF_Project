from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    telephone = models.CharField(max_length=15, verbose_name='Телефон')
    town = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

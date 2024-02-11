from django.db import models
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson
import datetime

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    telephone = models.CharField(max_length=15, verbose_name='Телефон')
    town = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    PAYMENT_METHOD = [
        ('cash', 'Оплата наличными'),
        ('transfer', 'Перевод')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата платежа')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.PositiveSmallIntegerField(verbose_name='Сумма платежа')
    payment_method = models.CharField(choices=PAYMENT_METHOD, verbose_name='Способ оплаты')

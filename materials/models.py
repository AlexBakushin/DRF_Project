from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    course_name = models.CharField(max_length=150, verbose_name='Название курса')
    course_description = models.TextField(verbose_name='Описание курса')
    course_preview = models.ImageField(upload_to='materials/', verbose_name='Аватар', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=150, verbose_name='Название курса')
    lesson_description = models.TextField(verbose_name='Описание курса')
    lesson_preview = models.ImageField(upload_to='materials/', verbose_name='Аватар', **NULLABLE)
    lesson_link = models.URLField(verbose_name='Ссылка на урок')
    course = models.ForeignKey(Course, verbose_name='Курсы', on_delete=models.CASCADE, **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Пользователь')

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='Пользователь')
    course = models.ForeignKey(Course, verbose_name='Курс', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Цена', default=5000)
    is_paid = models.BooleanField(verbose_name='Оплачено', default=False)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

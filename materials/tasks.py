from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from users.models import User


@shared_task
def update_notification(user_email, course_name):
    """
    Оповещает пользователя об обновлении курса
    """
    send_mail(
        subject='Обновление курса',
        message=f'Добрый день! Курс {course_name} обновлен. \n Посмотрите что нового в курсе.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
    print(f'Оповещение о курсе {course_name} отправлено пользователю {user_email}')


def check_last_login_user(last_login):
    """
    Если пользователь не заходил в систему более месяца - меняет is_active на False
    """
    if last_login < datetime.now() - timedelta(days=30):
        User.objects.filter(last_login=last_login).update(is_active=False)

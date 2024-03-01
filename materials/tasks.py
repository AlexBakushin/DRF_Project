from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def update_notification(user_email, course_name):
    send_mail(
        subject='Обновление курса',
        message=f'Добрый день! Курс {course_name} обновлен. \n Посмотрите что нового в курсе.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )

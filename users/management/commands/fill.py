from django.core.management import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment = Payment.objects.create(
            user=User.objects.get(id=1),
            payment_date=datetime.datetime.now(),
            course=Course.objects.get(id=1),
            payment_amount=10000,
            payment_method='transfer'
        )
        payment.save()

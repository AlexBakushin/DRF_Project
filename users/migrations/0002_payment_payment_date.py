# Generated by Django 4.2.7 on 2024-02-11 10:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 11, 15, 8, 34, 540314), verbose_name='Дата платежа'),
        ),
    ]

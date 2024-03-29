# Generated by Django 4.2.7 on 2024-03-15 10:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 15, 15, 54, 25, 695100), verbose_name='Дата платежа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 15, 15, 54, 25, 693059), verbose_name='Дата последнего входа'),
        ),
    ]

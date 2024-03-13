# Generated by Django 4.2.7 on 2024-03-13 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_payment_payment_date_alter_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 13, 16, 37, 54, 108414), verbose_name='Дата платежа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 13, 16, 37, 54, 105250), verbose_name='Дата последнего входа'),
        ),
    ]

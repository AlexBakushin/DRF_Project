# Generated by Django 4.2.7 on 2024-02-19 09:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 19, 14, 28, 11, 134993), verbose_name='Дата платежа'),
        ),
    ]
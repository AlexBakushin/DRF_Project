# Generated by Django 4.2.7 on 2024-02-24 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_alter_lesson_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.IntegerField(default=50, verbose_name='Цена'),
        ),
    ]
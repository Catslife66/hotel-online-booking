# Generated by Django 4.2.1 on 2023-05-17 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_booking_is_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='is_history',
            field=models.BooleanField(),
        ),
    ]

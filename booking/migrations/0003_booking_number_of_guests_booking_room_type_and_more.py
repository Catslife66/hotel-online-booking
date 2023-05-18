# Generated by Django 4.2.1 on 2023-05-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_remove_booking_room_alter_booking_user_bookingroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='number_of_guests',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='room_type',
            field=models.CharField(default='Superior Room', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
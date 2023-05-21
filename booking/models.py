import datetime

from django.conf import settings
from django.db import models

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from room.models import Room, Stock

User = settings.AUTH_USER_MODEL

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    room_type = models.CharField(max_length=20)
    number_of_guests = models.PositiveIntegerField()
    guest_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"Booking No.{self.id} - {self.created_at} - {self.is_paid}"
    

    @property
    def length_of_stay(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return None

    @property
    def cancel_status(self):
        if self.is_cancelled:
            return 'Cancelled'
        else:
            return 'Confirmed'
    

class BookingRoom(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_rooms')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking no.{self.booking.id} - {self.room.roomtype} - {self.room.date} - {self.booking.is_paid}"


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance, created, *args, **kwargs):
    print('booking_post_save')
    if instance.is_cancelled:
        booking_rooms = instance.booking_rooms.all()
        for booking_room in booking_rooms:
            room = booking_room.room
            room.stock.number_of_rooms += 1
            room.stock.save()

            if room.stock.number_of_rooms > 0:
                room.is_available = True
            room.save()


@receiver(post_save, sender=BookingRoom)
def room_stock_post_save(sender, instance, created, *args, **kwargs):
    print('room_stock_post_save')
    if created:
        room = instance.room
        room.stock.number_of_rooms -= 1
        room.stock.save()

        if room.stock.number_of_rooms == 0:
            room.is_available = False
        room.save()

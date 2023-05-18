from django.contrib import admin

from .models import Booking, BookingRoom

admin.site.register(Booking)

admin.site.register(BookingRoom)
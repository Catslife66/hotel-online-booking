from datetime import datetime

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect

from .forms import BookingForm
from .models import BookingRoom, Booking
from room.models import Room, RoomType


@login_required
def booking_view(request, check_in, check_out, room_type, pax):
    user = request.user.id
    info = {'check_in': check_in, 'check_out': check_out, 'room_type': room_type, 'pax': pax}
    rooms = Room.objects.search_available(check_in, check_out, room_type)
    type_of_room = RoomType.objects.get(id=info['room_type'])
    total_price = rooms.aggregate(total=Sum('price_per_night'))['total']

    # check the length of stays is same as length of available room queryset
    in_date = datetime.strptime(info['check_in'], '%Y-%m-%d').date()
    out_date = datetime.strptime(info['check_out'], '%Y-%m-%d').date()
    los = (out_date - in_date).days

    form = BookingForm(request.POST or None)
    if rooms.count() == los:
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user_id = user
            booking.check_in = check_in
            booking.check_out = check_out
            booking.room_type = type_of_room.title
            booking.number_of_guests = pax
            booking.total_price = total_price
            booking.save()
        
            booking_id = booking.id
            booking_rooms = [BookingRoom.objects.create(booking_id=booking.id, room=room) for room in rooms]
            for booking_room in booking_rooms:
                booking_room.booking_id = booking_id

            next_url = reverse('booking:booking-success', kwargs={'pk': booking.id})
            return redirect(next_url)
            
        context = {'info': info, 'form': form, 'los': los, 'type_of_room': type_of_room, 'total_price': total_price}
        return render(request, 'booking/booking-form.html', context)
    else:
        return HttpResponse('Something went wrong. Please go back to the home page.')



def booking_success(request, pk):
    messages.success(request, 'Your booking is confirmed.')
    booking = Booking.objects.get(pk=pk)
    context = {'booking': booking}
    return render(request, 'booking/booking-success.html', context)


@login_required
def booking_list(request, pk):
    history_bookings = Booking.objects.filter(Q(user_id=pk) & Q(check_out__lte=datetime.today()))
    coming_bookings = Booking.objects.filter(Q(user_id=pk) & Q(check_in__gte=datetime.today()))
    context = {'history_bookings': history_bookings, 'coming_bookings': coming_bookings}
    return render(request, 'booking/booking-list.html', context)


def booking_detail(request, pk):
    booking = Booking.objects.get(id=pk)
    return render(request, 'booking/booking-detail.html', {'booking': booking})


@login_required
def update_booking_detail(request, pk):
    booking = Booking.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'The detail is saved.')
            user_bookings = reverse('booking:booking-list', kwargs={'pk': request.user.id})
            return redirect(user_bookings)
    else:
        form = BookingForm(instance=booking)

    context = {'form': form}
    return render(request, 'booking/booking-update.html', context)


@login_required
def cancel_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    booking.is_cancelled = True
    booking.save()
    return render(request, 'booking/booking-cancel.html', {'booking':booking})

    


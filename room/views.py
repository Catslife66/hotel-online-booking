import datetime

from django.shortcuts import render
from django.urls import reverse

from .models import Room, RoomType


def room_list_view(request):
    obj_list = RoomType.objects.all()
    td = datetime.date.today()
    context = {'obj_list': obj_list, 'td': td }
    return render(request, 'room/room_list.html', context)


def search(request):
    check_in = request.GET.get('check-in')
    check_out = request.GET.get('check-out')
    room_type = request.GET.get('room-type')
    pax = request.GET.get('pax')

    search_info = {
        'check_in':check_in,
        'check_out':check_out,
        'room_type':room_type,
        'pax': pax
        }

    available_list = Room.objects.search_available(check_in, check_out, room_type)
    booking_url = reverse('booking:booking-form', args=[check_in, check_out, room_type, pax])
    unavailable_list = Room.objects.filter_unavailable(check_in, check_out, room_type)
    
    context = {
        'available_list': available_list,
        'search_info': search_info,
        'booking_url': booking_url,
        'unavailable_list': unavailable_list,
    }

    return render(request, 'room/room-search.html', context)


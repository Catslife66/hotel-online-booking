from django.urls import path

from . import views

app_name = 'booking'
urlpatterns = [
    path('check-in=<str:check_in>&check-out=<str:check_out>&room-type=<str:room_type>&pax=<int:pax>/', views.booking_view, name='booking-form'),
    path('booking-<int:pk>/', views.booking_detail, name='booking-detail'),
    path('booking-<int:pk>/cancel/', views.cancel_booking, name='booking-cancel'),
    path('booking-<int:pk>/update/', views.update_booking_detail, name='booking-update'),
    path('booking-<int:pk>/success/', views.booking_success, name='booking-success'),
    path('bookings/user-<int:pk>/', views.booking_list, name='booking-list'),
]
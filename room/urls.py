from django.urls import path

from . import views

app_name = 'room'
urlpatterns = [
    path('', views.room_list_view, name='room-list'),
    path('search/', views.search, name='search'),
]
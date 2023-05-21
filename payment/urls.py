from django.urls import path

from . import views

app_name = 'payment'
urlpatterns = [
    path('create-payment-intent/', views.create_payment, name='create-payment'),
]
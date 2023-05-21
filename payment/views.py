import json
import stripe

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from booking.models import Booking

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        booking_id = json.loads(request.body)
        booking_obj = Booking.objects.get(id=booking_id)
        total = booking_obj.total_price
        total = '{:.2f}'.format(total)
        total = total.replace('.', '')
        total = int(total)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency='gbp',
            metadata={
                'user_id': request.user.id,
                'booking_id': booking_id
            }
        )
        return JsonResponse({
            'stripeKey': settings.STRIPE_PUBLIC_KEY,
            'clientSecret': intent.client_secret,
        })
        

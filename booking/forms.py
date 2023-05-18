from typing import Any, Dict
from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))
    class Meta:
        model = Booking
        fields = ('guest_name', 'email', 'phone')

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
        
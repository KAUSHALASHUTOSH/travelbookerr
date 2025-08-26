from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Booking

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']

    # Custom validation for number of seats
    def clean_number_of_seats(self):
        seats = self.cleaned_data.get('number_of_seats')
        if seats <= 0:
            raise forms.ValidationError("You must book at least one seat.")
        return seats

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

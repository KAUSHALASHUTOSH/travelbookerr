import os
import sys
import site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TravelOption, Booking
from .forms import UserRegisterForm, BookingForm, UserUpdateForm

def home(request):
    travels = TravelOption.objects.all()
    if request.GET.get('type'):
        travels = travels.filter(type=request.GET['type'])
    if request.GET.get('source'):
        travels = travels.filter(source__icontains=request.GET['source'])
    if request.GET.get('destination'):
        travels = travels.filter(destination__icontains=request.GET['destination'])

    # The logic to check for existing confirmed bookings has been removed
    booked_travel_ids = []
    if request.user.is_authenticated:
        pass  # This part is now empty, allowing multiple bookings

    context = {
        'travels': travels,
        'booked_travel_ids': booked_travel_ids
    }
    return render(request, 'travel_list.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def book_travel(request, travel_id):
    travel = get_object_or_404(TravelOption, pk=travel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data['number_of_seats']
            if seats <= travel.available_seats:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.travel_option = travel
                booking.total_price = seats * travel.price
                booking.status = 'Confirmed'
                booking.save()
                travel.available_seats -= seats
                travel.save()
                messages.success(request, 'Your booking has been confirmed!')
                return redirect('my_bookings')
            else:
                messages.error(request, 'Not enough seats available.')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form, 'travel': travel})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings_list.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    booking.status = 'Cancelled'
    booking.save()
    booking.travel_option.available_seats += booking.number_of_seats
    booking.travel_option.save()
    messages.info(request, 'Your booking has been cancelled.')
    return redirect('my_bookings')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

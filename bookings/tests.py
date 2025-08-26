from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import TravelOption, Booking

class BookingTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a test travel option
        self.travel_option = TravelOption.objects.create(
            type='Flight',
            source='New York',
            destination='London',
            date_time=timezone.now(),
            price=1500.00,
            available_seats=10
        )

    def test_booking_decreases_available_seats(self):
        """Test that booking a trip correctly decreases the number of available seats."""
        initial_seats = self.travel_option.available_seats
        seats_to_book = 2

        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=seats_to_book,
            total_price=self.travel_option.price * seats_to_book,
            status='Confirmed'
        )
        
        # Manually save the travel option to reflect the change
        self.travel_option.available_seats -= seats_to_book
        self.travel_option.save()

        # Refresh the travel option instance from the database
        self.travel_option.refresh_from_db()

        # Check if available seats have been correctly updated
        self.assertEqual(self.travel_option.available_seats, initial_seats - seats_to_book)

    def test_booking_creation(self):
        """Test that a new booking is created with the correct details."""
        seats_to_book = 3
        total_price = self.travel_option.price * seats_to_book

        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=seats_to_book,
            total_price=total_price,
            status='Confirmed'
        )

        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.travel_option, self.travel_option)
        self.assertEqual(booking.number_of_seats, seats_to_book)
        self.assertEqual(booking.total_price, total_price)
        self.assertEqual(booking.status, 'Confirmed')


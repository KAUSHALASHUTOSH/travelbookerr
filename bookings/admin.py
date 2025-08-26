from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import TravelOption, Booking


# ========= BOOKING INLINE (for TravelOption & User) =========
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ("user", "number_of_seats", "status", "total_price", "booking_date")
    can_delete = False
    verbose_name_plural = "Bookings for this Trip"
    ordering = ("-booking_date",)   # Show latest first


# ========= ACTIONS =========
@admin.action(description="Increase available seats by 10")
def increase_seats(modeladmin, request, queryset):
    for obj in queryset:
        obj.available_seats += 10
        obj.save()


@admin.action(description="Mark selected bookings as Cancelled")
def mark_as_cancelled(modeladmin, request, queryset):
    queryset.update(status="Cancelled")


# ========= TRAVEL OPTION ADMIN =========
@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ("type", "source", "destination", "date_time", "price", "available_seats")
    list_filter = ("type", "source", "destination", "date_time")
    search_fields = ("source", "destination")
    ordering = ("date_time",)
    inlines = [BookingInline]
    actions = [increase_seats]

    # Group fields in the form
    fieldsets = (
        ("Travel Details", {
            "fields": ("type", "source", "destination", "date_time")
        }),
        ("Pricing & Capacity", {
            "fields": ("price", "available_seats")
        }),
    )


# ========= BOOKING ADMIN =========
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "travel_option", "number_of_seats", "total_price", "status", "booking_date")
    list_filter = ("status", "booking_date")
    search_fields = ("user__username", "travel_option__source", "travel_option__destination")
    autocomplete_fields = ("user", "travel_option")
    actions = [mark_as_cancelled]
    date_hierarchy = "booking_date"

    fieldsets = (
        ("Booking Information", {
            "fields": ("user", "travel_option")
        }),
        ("Seats & Payment", {
            "fields": ("number_of_seats", "total_price")
        }),
        ("Status & Date", {
            "fields": ("status", "booking_date")
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-calc total price if not manually set"""
        if obj.travel_option and obj.number_of_seats:
            obj.total_price = obj.travel_option.price * obj.number_of_seats
        super().save_model(request, obj, form, change)


# ========= CUSTOM USER ADMIN (with booking inline) =========
class UserBookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ("travel_option", "number_of_seats", "total_price", "status", "booking_date")
    can_delete = False
    ordering = ("-booking_date",)


class CustomUserAdmin(DefaultUserAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser", "last_login")
    inlines = [UserBookingInline]


# Unregister default User admin & register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ========= BRANDING =========
admin.site.site_header = "TravelBooker Admin Dashboard"
admin.site.site_title = "TravelBooker Admin"
admin.site.index_title = "Manage Travel Options, Bookings, and Users"
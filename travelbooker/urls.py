from django.contrib import admin
from django.urls import path, include
from bookings import views   # <-- import your views
from django.contrib.auth import views as auth_views  # <-- import auth views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("book/<int:travel_id>/", views.book_travel, name="book_travel"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("profile/", views.profile, name="profile"), # Added profile URL
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
]

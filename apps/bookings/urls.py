from django.urls import path
from . import views

urlpatterns = [
    path('api/dashboard/booking-stats/', views.get_booking_stats, name='booking_stats'),
] 
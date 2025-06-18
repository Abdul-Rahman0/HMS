from django.urls import path
from . import views

urlpatterns = [
    path('api/dashboard/room-stats/', views.get_room_stats, name='room_stats'),
    path('api/dashboard/guest-stats/', views.guest_dashboard_stats, name='guest_dashboard_stats'),
] 
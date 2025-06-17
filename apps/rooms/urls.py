from django.urls import path
from . import views

urlpatterns = [
    path('api/dashboard/room-stats/', views.get_room_stats, name='room_stats'),
] 
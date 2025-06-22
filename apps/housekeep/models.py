from django.db import models
from django.utils import timezone
from apps.rooms.models import Room  # adjust import path as needed
from django.contrib.auth import get_user_model

User = get_user_model()

class HouseKeepingLog(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='cleaning_logs')
    cleaned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cleaned_at = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Log {self.id} - Room {self.room.room_number}"
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from django.utils.html import format_html

from .models import HouseKeepingLog
from apps.rooms.models import Room

User = get_user_model()

@admin.register(HouseKeepingLog)
class HouseKeepingLogAdmin(admin.ModelAdmin):
    list_display = ('room', 'cleaned_by', 'cleaned_at', 'short_notes', 'remaining_rooms_display')
    list_filter = ('cleaned_at', 'room')
    search_fields = ('room__room_number', 'notes')
    readonly_fields = ('remaining_rooms_display',)

    # 👉 1. Show only rooms not cleaned today in Add Form
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        today = timezone.now().date()
        if db_field.name == "room":
            cleaned_room_ids = HouseKeepingLog.objects.filter(cleaned_at=today).values_list('room_id', flat=True)
            kwargs["queryset"] = Room.objects.exclude(id__in=cleaned_room_ids)
        if db_field.name == "cleaned_by":
            try:
                group = Group.objects.get(name="Housekeeping")
                kwargs["queryset"] = User.objects.filter(groups=group)
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # 👉 2. Show Remaining Room Count as a Field in Each Row (same value for all rows)
    def remaining_rooms_display(self, obj):
        today = timezone.now().date()
        total_rooms = Room.objects.count()
        cleaned_rooms = HouseKeepingLog.objects.filter(cleaned_at=today).values_list('room_id', flat=True).distinct().count()
        remaining = total_rooms - cleaned_rooms
        return format_html('<b>{}</b> rooms remaining today', remaining)
    remaining_rooms_display.short_description = "Remaining Today"

    def short_notes(self, obj):
        return (obj.notes[:50] + '...') if obj.notes else ''
    short_notes.short_description = 'Notes'

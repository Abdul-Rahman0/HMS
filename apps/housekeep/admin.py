from django.contrib import admin
from .models import HouseKeepingLog

@admin.register(HouseKeepingLog)
class HouseKeepingLog(admin.ModelAdmin):
    list_display = ('room', 'cleaned_by', 'cleaned_at', 'short_notes')
    list_filter = ('cleaned_at', 'room')
    search_fields = ('room__room_number', 'notes')

    def short_notes(self, obj):
        return obj.notes[:50] + '...' if obj.notes and len(obj.notes) > 50 else obj.notes
    short_notes.short_description = 'Notes'

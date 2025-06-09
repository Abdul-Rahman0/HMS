from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('student__user__username', 'room__room_number')

    def student_name(self, obj):
        return obj.student.user.username
    student_name.short_description = 'Student'

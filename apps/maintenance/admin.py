from django.contrib import admin
from .models import MaintenanceStaff , MaintenanceRequest

@admin.register(MaintenanceStaff)
class MaintenanceStaffAdmin(admin.ModelAdmin):
    list_display = [('user')]
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('room', 'issue', 'status', 'assigned_to', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('room__room_number', 'issue', 'assigned_to__username', 'student__username', 'staff__username')

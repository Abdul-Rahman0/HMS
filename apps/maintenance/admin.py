from django.contrib import admin
from .models import MaintenanceStaff , MaintenanceRequest , Receptionist
from apps.accounts.models import StudentProfile,User


@admin.register(MaintenanceStaff)
class MaintenanceStaffAdmin(admin.ModelAdmin):
    list_display = [('user')]
    
@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = [('user')]
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('room', 'issue', 'status', 'assigned_to', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('room__room_number', 'issue', 'assigned_to__username', 'student__username', 'staff__username')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(groups__name="Maintenance")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
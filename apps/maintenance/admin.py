from .models import MaintenanceStaff , MaintenanceRequest , Receptionist
from apps.accounts.models import StudentProfile,User
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import admin, messages


@admin.register(MaintenanceStaff)
class MaintenanceStaffAdmin(admin.ModelAdmin):
    list_display = ['user',"student","issue_fixed","mark_complete_button"]
    def student(self, obj):
        return obj.user.student
    student.short_description = 'Student'
    
    def issue_fixed(self, obj):
        return obj.user.request_complete
    issue_fixed.short_description = 'Issue Status'
    issue_fixed.boolean = True  # ✅ This makes it show ✓ or ✗
    
     # ✅ 1. Custom Button in List View
    def mark_complete_button(self, obj):
        if not obj.user.request_complete:
            return format_html(
             '<a class="button" style="color: white; background-color: #218838; padding: 5px 10px; text-decoration: none; border-radius: 4px;" href="{}">Completed</a>&nbsp;',
            f'mark-completed/{obj.pk}'
        )
        else:
            return "-"
    mark_complete_button.short_description = 'Mark Completed'
    mark_complete_button.allow_tags = True

    # ✅ 2. Add Custom URL
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('mark-completed/<int:pk>', self.admin_site.admin_view(self.mark_completed_action), name='mark-completed'),
        ]
        return custom_urls + urls

    # ✅ 3. Custom View Logic
    def mark_completed_action(self, request, pk):
        staff = MaintenanceStaff.objects.get(pk=pk)
        if staff.user:
            staff.user.request_complete = True
            staff.user.save()
            self.message_user(request, "Issue marked as completed ✅", messages.SUCCESS)
        else:
            self.message_user(request, "Request not found ❌", messages.ERROR)
        return redirect(request.META.get('HTTP_REFERER'))
    
    
    
# @admin.register(Receptionist)
# class ReceptionistAdmin(admin.ModelAdmin):
#     list_display = [('user')]
    
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('room', 'issue', 'status', 'assigned_to', 'created_at', 'resolved_at')
    list_filter = ('status', 'created_at')
    search_fields = ('room__room_number', 'issue', 'assigned_to__username', 'student__username', 'staff__username')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(groups__name="Maintenance")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Only insert MaintenanceStaff on CREATE, not UPDATE
        if not change:
            MaintenanceStaff.objects.create(user=obj)
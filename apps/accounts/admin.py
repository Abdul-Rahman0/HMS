from django.contrib import admin
from .models import User, StudentProfile, HostelApplication, HostelCertificate
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
# User Register model

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'group', 'is_active', 'action_buttons')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'group', 'is_active'),
        }),
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'group', 'is_active')
        }),
        ('Additional Info', {
            'fields': ('phone_number', 'address', 'date_of_birth', 'profile_picture')
        }),
        ('Guardian Info', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_email')
        }),
    )
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # custom css ka path
        }
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/approve/', self.admin_site.admin_view(self.approve_user), name='approve_user'),
            path('<int:user_id>/reject/', self.admin_site.admin_view(self.reject_user), name='reject_user'),
        ]
        return custom_urls + urls

    def approve_user(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        user.is_active = True
        user.is_staff = True
        user.save()
        self.message_user(request, f'User {user.username} approved ✅', messages.SUCCESS)
        return redirect('/admin/accounts/user/')

    def reject_user(self, request, user_id):
        user = self.model.objects.get(pk=user_id)
        user.is_active = False
        user.is_staff = False
        user.save()
        self.message_user(request, f'User {user.username} rejected ❌', messages.ERROR)
        return redirect('/admin/accounts/user/')

    def action_buttons(self, obj):
        return format_html(
            '<a class="button" style="color: white; background-color: #218838; padding: 5px 10px; text-decoration: none; border-radius: 4px;" href="{}">Approve</a>&nbsp;'
            '<a class="button" style="color: white; background-color: red; padding: 5px 10px; text-decoration: none; border-radius: 4px;" href="{}">Reject</a>',
            f'/admin/accounts/user/{obj.pk}/approve/',
            f'/admin/accounts/user/{obj.pk}/reject/',
        )
    action_buttons.short_description = 'Student Status'
    
    def save_model(self, request, obj, form, change):
        # First save the user
        super().save_model(request, obj, form, change)
        
        # Then handle group assignment
        if obj.group:
            # Clear existing groups
            obj.groups.clear()
            # Add the new group
            obj.groups.add(obj.group)
            # Set is_staff to True if user has a group
            obj.is_staff = True
            obj.save()

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect("/admin/accounts/user/")
    
   

# Student profile model 

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'enrollment_date',
        'guardian_name',
        'address',
        'room_assigned',
    )
    list_display = ('user',
        'enrollment_date',
        'guardian_name',
        'address',
        'room_assigned',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__groups__name='Student')  # Filter only those with 'Student' group
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(groups__name="Student")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# Register your models here.


# admin.site.register(StaffProfile)
admin.site.register(HostelApplication)
admin.site.register(HostelCertificate)

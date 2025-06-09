from django.contrib import admin
from .models import User, StudentProfile, StaffProfile, HostelApplication, HostelCertificate
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
# User Register model

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'guardian_name', 'guardian_phone', 'guardian_email')}),
        ('Permissions', {'fields': ('is_active','group')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'group','is_active','action_buttons')
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
    
    
    
    
    # def save_model(self, request, obj, form, change):
    #     # ✅ Agar group assign hai to is_staff ko True karo
    #     if obj.group:
    #         obj.is_staff = True
    #         obj.save()  # 👈 Pehle hi save kiya ja raha hai to dobara karna optional hai

    #         # ✅ Django built-in groups me bhi set karo
    #         obj.groups.set([obj.group])

    #     # 🔁 Super call at the end to ensure full save
    #     super().save_model(request, obj, form, change)

            





# Student profile model 

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'student_id',
        'enrollment_date',
        'guardian_name',
        'address',
        'room_assigned',
    )


# Register your models here.


admin.site.register(StaffProfile)
admin.site.register(HostelApplication)
admin.site.register(HostelCertificate)

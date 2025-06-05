from django.contrib import admin
from .models import User, StudentProfile, StaffProfile, HostelApplication, HostelCertificate


# User Register model

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'guardian_name', 'guardian_phone', 'guardian_email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)







# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(StaffProfile)
admin.site.register(HostelApplication)
admin.site.register(HostelCertificate)

from django.contrib import admin
from .models import User, StudentProfile, StaffProfile, HostelApplication, HostelCertificate

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(StaffProfile)
admin.site.register(HostelApplication)
admin.site.register(HostelCertificate)

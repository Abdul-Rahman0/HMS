from django.contrib.auth.models import AbstractUser,Group
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


   

class User(AbstractUser):
    
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_users',
        verbose_name="Role",
        help_text=_('Assign a group to this user'),
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.group:
            self.groups.set([self.group])

    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    enrollment_date = models.DateField(null=True, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)  # Already present
    phone = models.CharField(max_length=15, blank=True, null=True)
    course = models.CharField(max_length=100)
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    room_assigned = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Profile"

class HostelApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.status}"


class HostelCertificate(models.Model):
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    issued_date = models.DateField(default=timezone.now)
    download_link = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"Certificate #{self.id} - {self.student.user.username}"

    def generate_certificate(self):
        # Simulate generation
        self.download_link = f"/media/certificates/{self.student.user.username}_certificate.pdf"
        self.save()
        return self.download_link

    def view_certificate(self):
        return self.download_link

    def download_certificate(self):
        return self.download_link


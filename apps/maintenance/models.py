# apps/maintenance/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.rooms.models import Room  # adjust import as needed
from apps.accounts.models import StudentProfile,User

User = get_user_model()

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receptionist_profile')
    


#  Maintenance request

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests')
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_maintenance_requests')
    issue = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_maintenance_requests')
    created_at = models.DateField(auto_now_add=True)
    resolved_at = models.DateField(null=True, blank=True)
    request_create = models.BooleanField(default=False)
    request_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Request #{self.id} for Room {self.room.room_number}"

    # -----------------------------
    #          METHODS
    # -----------------------------

    def submit_request(self):
        self.status = 'open'
        self.created_at = timezone.now()
        self.save()

    def assign_request_to_staff(self, staff_id):
        staff_member = User.objects.filter(id=staff_id, is_staff=True).first()
        if staff_member:
            self.assigned_to = staff_member
            self.status = 'in_progress'
            self.save()
            return True
        return False

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            if new_status == 'completed':
                self.resolved_at = timezone.now()
            self.save()
            return True
        return False

    def close_request(self):
        self.status = 'completed'
        self.resolved_at = timezone.now()
        self.save()


class MaintenanceStaff(models.Model):
    user = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE, related_name='maintenance_requests')
    

    def __str__(self):
        return f"{self.user.username} (Maintenance ID: {self.id})"
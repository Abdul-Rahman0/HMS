from django.db import models
from apps.accounts.models import User
from apps.rooms.models import Room
from django.conf import settings

# Create your models here.

class MaintenanceRequest(models.Model):
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null=True,
        blank=True,)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Maintenance Request for Room {self.room.room_number} by {self.submitted_by.username}"

class MaintenanceComment(models.Model):
    maintenance_request = models.ForeignKey(
        MaintenanceRequest,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='maintenance_comments'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Request {self.maintenance_request.id}"

    class Meta:
        ordering = ['created_at']

class MaintenanceAttachment(models.Model):
    maintenance_request = models.ForeignKey(
        MaintenanceRequest,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='maintenance_attachments/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='maintenance_attachments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Request {self.maintenance_request.id}"

    class Meta:
        ordering = ['-created_at']

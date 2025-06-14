from django.db import models
from django.utils import timezone
from apps.accounts.models import StudentProfile  # adjust based on your project

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,null=True,blank=False)
    room_number = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES , null=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Room {self.room_number} ({self.get_type_display()})"
     # ✅ Method 1: Check if room is available
    def is_available(self):
        return self.status == 'available'

    # ✅ Method 2: Update room status
    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            self.save()
        else:
            raise ValueError(f"Invalid status: {new_status}")
        
        
        
# Guest Log



class GuestLog(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(null=True, blank=True)
    associated_student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Guest: {self.name} (Student: {self.associated_student.user.username})"

    def log_guest(self, name, purpose):
        return GuestLog.objects.create(
            name=name,
            purpose=purpose,
            associated_student=self.associated_student,
            check_in_time=timezone.now()
        )

    @classmethod
    def view_guest_log(cls, start_date, end_date):
        return cls.objects.filter(check_in_time__range=(start_date, end_date))

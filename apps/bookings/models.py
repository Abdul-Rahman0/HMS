# from django.db import models
# from django.core.validators import MinValueValidator
# from django.utils import timezone
# from apps.accounts.models import User
# from apps.rooms.models import Room
# from django.conf import settings

# # class Booking(models.Model):
# #     class BookingStatus(models.TextChoices):
# #         PENDING = 'PENDING', 'Pending'
# #         APPROVED = 'APPROVED', 'Approved'
# #         REJECTED = 'REJECTED', 'Rejected'
# #         CANCELLED = 'CANCELLED', 'Cancelled'
# #         COMPLETED = 'COMPLETED', 'Completed'

# #     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# #     room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
# #     check_in_date = models.DateField()
# #     check_out_date = models.DateField()
# #     status = models.CharField(
# #         max_length=20,
# #         choices=BookingStatus.choices,
# #         default=BookingStatus.PENDING
# #     )
# #     total_amount = models.DecimalField(
# #         max_digits=10,
# #         decimal_places=2
# #     )
# #     deposit_amount = models.DecimalField(
# #         max_digits=10,
# #         decimal_places=2,
# #         default=0
# #     )
# #     special_requests = models.TextField(blank=True)
# #     is_active = models.BooleanField(default=True)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     def __str__(self):
# #         return f"Booking for {self.student.username} in Room {self.room.room_number}"

# #     class Meta:
# #         ordering = ['-created_at']

# class BookingCancellation(models.Model):
#     booking = models.ForeignKey(
#         Booking,
#         on_delete=models.CASCADE,
#         related_name='cancellations'
#     )
#     cancellation_date = models.DateTimeField(auto_now_add=True)
#     reason = models.TextField()
#     refund_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True
#     )
#     is_refunded = models.BooleanField(default=False)
#     refund_date = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Cancellation for Booking {self.booking.id}"

#     class Meta:
#         ordering = ['-cancellation_date']

# class HostelCertificate(models.Model):
#     booking = models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True)
#     file = models.FileField(upload_to='certificates/')
#     generated_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Certificate for Booking {self.booking.id}"



from django.db import models
from apps.accounts.models import StudentProfile  # adjust app name as needed
from apps.rooms.models import Room     # adjust app name as needed
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(default=timezone.now)
    check_out = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Booking #  {self.student.user.username} - {self.room.room_number}"
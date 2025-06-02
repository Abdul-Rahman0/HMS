from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Room(models.Model):
    class RoomType(models.TextChoices):
        SINGLE = 'SINGLE', 'Single'
        DOUBLE = 'DOUBLE', 'Double'
        TRIPLE = 'TRIPLE', 'Triple'
        QUAD = 'QUAD', 'Quad'

    class RoomStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        OCCUPIED = 'OCCUPIED', 'Occupied'
        MAINTENANCE = 'MAINTENANCE', 'Under Maintenance'
        RESERVED = 'RESERVED', 'Reserved'

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(
        max_length=10,
        choices=RoomType.choices,
        default=RoomType.DOUBLE
    )
    floor = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    status = models.CharField(
        max_length=20,
        choices=RoomStatus.choices,
        default=RoomStatus.AVAILABLE
    )
    price_per_month = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(blank=True)
    amenities = models.JSONField(default=dict)  # Store amenities as JSON
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    allocated_student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocated_room')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"

    class Meta:
        ordering = ['floor', 'room_number']

class RoomImage(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='room_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Room {self.room.room_number}"

    class Meta:
        ordering = ['-is_primary', 'created_at']

class RoomMaintenance(models.Model):
    class MaintenanceType(models.TextChoices):
        ROUTINE = 'ROUTINE', 'Routine'
        REPAIR = 'REPAIR', 'Repair'
        RENOVATION = 'RENOVATION', 'Renovation'
        EMERGENCY = 'EMERGENCY', 'Emergency'

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )
    maintenance_type = models.CharField(
        max_length=20,
        choices=MaintenanceType.choices
    )
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance for Room {self.room.room_number} - {self.get_maintenance_type_display()}"

    class Meta:
        ordering = ['-start_date']

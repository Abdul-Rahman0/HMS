from django.db import models
from django.utils import timezone
from apps.accounts.models import StudentProfile

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    ]

    PAYMENT_STATUS = [
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    
    student = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True,default=0.0)
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS,null=True, blank=True)
    payment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)

    
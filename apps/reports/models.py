from django.db import models

# Create your models here.

class Report(models.Model):
    REPORT_TYPES = [
        ('occupancy', 'Occupancy Report'),
        ('payments', 'Payments Report'),
        ('maintenance', 'Maintenance Report'),
    ]
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='reports/')

    def __str__(self):
        return f"{self.report_type} - {self.generated_at}"

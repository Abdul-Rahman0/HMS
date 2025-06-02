from django.db import models
from apps.accounts.models import User
from apps.bookings.models import Booking

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Cash'
        CREDIT_CARD = 'CREDIT_CARD', 'Credit Card'
        DEBIT_CARD = 'DEBIT_CARD', 'Debit Card'
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'
        UPI = 'UPI', 'UPI'
        WALLET = 'WALLET', 'Wallet'

    class PaymentType(models.TextChoices):
        RENT = 'RENT', 'Rent'
        DEPOSIT = 'DEPOSIT', 'Deposit'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'
        LATE_FEE = 'LATE_FEE', 'Late Fee'
        OTHER = 'OTHER', 'Other'

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment_records'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PaymentType.choices
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    receipt_number = models.CharField(
        max_length=50,
        unique=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment of {self.amount} for Booking {self.booking.id}"

    class Meta:
        ordering = ['-payment_date']

class PaymentRefund(models.Model):
    class RefundStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        PROCESSED = 'PROCESSED', 'Processed'
        REJECTED = 'REJECTED', 'Rejected'

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=RefundStatus.choices,
        default=RefundStatus.PENDING
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='processed_refunds'
    )
    processed_date = models.DateTimeField(null=True, blank=True)
    refund_transaction_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Refund for Payment {self.payment.receipt_number}"

    class Meta:
        ordering = ['-created_at']

class PaymentReceipt(models.Model):
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name='receipt'
    )
    receipt_file = models.FileField(
        upload_to='payment_receipts/'
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    is_downloaded = models.BooleanField(default=False)
    downloaded_at = models.DateTimeField(null=True, blank=True)
    downloaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='downloaded_receipts'
    )

    def __str__(self):
        return f"Receipt for Payment {self.payment.receipt_number}"

    class Meta:
        ordering = ['-generated_at']

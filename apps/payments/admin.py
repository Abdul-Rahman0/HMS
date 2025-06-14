from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'method', 'payment_date', 'status')
    # Show all fields in a single section (no tabs, no collapsible fieldsets)
    fields = ('student', 'amount', 'method', 'status', 'payment_date')

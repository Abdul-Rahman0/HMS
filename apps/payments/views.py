from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Payment
from datetime import date
from django.db.models import Q

# Create your views here.

def monthly_fee_status(request):
    """
    API endpoint to get this month's paid and pending student fee counts
    """
    today = timezone.now().date()
    first_day = today.replace(day=1)
    last_day = today

    # Paid students this month
    paid_count = Payment.objects.filter(
        status='paid',
        payment_date__gte=first_day,
        payment_date__lte=last_day
    ).values('student').distinct().count()

    # Pending students (who have a pending payment this month)
    pending_count = Payment.objects.filter(
        status='pending',
        payment_date__gte=first_day,
        payment_date__lte=last_day
    ).values('student').distinct().count()

    return JsonResponse({
        'month': today.strftime('%B %Y'),
        'paid_students': paid_count,
        'pending_students': pending_count
    })

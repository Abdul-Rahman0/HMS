from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Booking

# Create your views here.

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_booking_stats(request):
    """
    API endpoint to get booking statistics for dashboard
    """
    try:
        today = timezone.now().date()
        first_day = today.replace(day=1)
        last_day = today

        # Total bookings
        total_bookings = Booking.objects.count()
        
        # Active bookings (this month)
        active_bookings = Booking.objects.filter(
            status='active',
            check_in__gte=first_day,
            check_in__lte=last_day
        ).count()
        
        # Completed bookings (this month)
        completed_bookings = Booking.objects.filter(
            status='completed',
            check_in__gte=first_day,
            check_in__lte=last_day
        ).count()
        
        # Cancelled bookings (this month)
        cancelled_bookings = Booking.objects.filter(
            status='cancelled',
            check_in__gte=first_day,
            check_in__lte=last_day
        ).count()
        
        # Today's bookings
        today_bookings = Booking.objects.filter(
            check_in=today
        ).count()

        data = {
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'today_bookings': today_bookings
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

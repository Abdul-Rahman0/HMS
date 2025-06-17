from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Room

# Create your views here.

@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_room_stats(request):
    try:
        # Get total rooms count
        total_rooms = Room.objects.count()
        
        # Get counts for each room status
        occupied_rooms = Room.objects.filter(status='occupied').count()
        available_rooms = Room.objects.filter(status='available').count()
        maintenance_rooms = Room.objects.filter(status='maintenance').count()

        data = {
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'available_rooms': available_rooms,
            'maintenance_rooms': maintenance_rooms
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

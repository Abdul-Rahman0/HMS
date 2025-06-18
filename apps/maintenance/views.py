from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import MaintenanceRequest
from django.core.serializers import serialize
import json

# Create your views here.

def maintenance_api_test(request):
    """
    View to serve the maintenance API test page
    """
    return render(request, 'maintenance_api_test.html')

@login_required
def maintenance_dashboard_stats(request):
    try:
        # Get total maintenance requests
        total_requests = MaintenanceRequest.objects.count()
        
        # Get completed requests
        completed_requests = MaintenanceRequest.objects.filter(status='completed').count()
        
        # Get open requests (pending)
        pending_requests = MaintenanceRequest.objects.filter(status='open').count()
        
        # Get in progress requests
        in_progress_requests = MaintenanceRequest.objects.filter(status='in_progress').count()
        
        data = {
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'pending_requests': pending_requests,
            'in_progress_requests': in_progress_requests
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_maintenance_requests(request):
    """
    API endpoint to get all maintenance requests with detailed information
    """
    try:
        # Get all maintenance requests with related data
        maintenance_requests = MaintenanceRequest.objects.select_related(
            'room', 'student__user', 'assigned_to'
        ).all().order_by('-created_at')
        
        requests_data = []
        
        for request in maintenance_requests:
            request_data = {
                'id': request.id,
                'room_number': request.room.room_number if request.room else None,
                'student_name': f"{request.student.user.first_name} {request.student.user.last_name}" if request.student and request.student.user else "N/A",
                'issue': request.issue,
                'status': request.status,
                'status_display': request.get_status_display(),
                'assigned_to': f"{request.assigned_to.first_name} {request.assigned_to.last_name}" if request.assigned_to else "Not Assigned",
                'created_at': request.created_at.strftime('%Y-%m-%d') if request.created_at else None,
                'resolved_at': request.resolved_at.strftime('%Y-%m-%d') if request.resolved_at else None,
                'request_create': request.request_create,
                'request_complete': request.request_complete
            }
            requests_data.append(request_data)
        
        # Get summary statistics
        total_requests = maintenance_requests.count()
        completed_requests = maintenance_requests.filter(status='completed').count()
        pending_requests = maintenance_requests.filter(status='open').count()
        in_progress_requests = maintenance_requests.filter(status='in_progress').count()
        
        response_data = {
            'success': True,
            'summary': {
                'total_requests': total_requests,
                'completed_requests': completed_requests,
                'pending_requests': pending_requests,
                'in_progress_requests': in_progress_requests
            },
            'requests': requests_data
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_maintenance_request(request):
    """
    API endpoint to create a new maintenance request
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['room_id', 'issue']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Create the maintenance request
        maintenance_request = MaintenanceRequest.objects.create(
            room_id=data['room_id'],
            student_id=data.get('student_id'),
            issue=data['issue'],
            status='open'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Maintenance request created successfully',
            'request_id': maintenance_request.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_maintenance_request(request, request_id):
    """
    API endpoint to update a maintenance request
    """
    try:
        data = json.loads(request.body)
        
        # Get the maintenance request
        maintenance_request = MaintenanceRequest.objects.get(id=request_id)
        
        # Update fields if provided
        if 'status' in data:
            maintenance_request.status = data['status']
        if 'assigned_to' in data:
            maintenance_request.assigned_to_id = data['assigned_to']
        if 'issue' in data:
            maintenance_request.issue = data['issue']
        
        maintenance_request.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Maintenance request updated successfully'
        })
        
    except MaintenanceRequest.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Maintenance request not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from ..accounts.models import StudentProfile # Assuming StudentProfile is in accounts app
from ..bookings.models import Booking, HostelCertificate
from ..payments.models import Payment
from ..maintenance.models import MaintenanceRequest
from ..rooms.models import Room # Assuming Room is in rooms app

# Import serializers (will need to create these later based on requirements)
from .serializers import (
    StudentProfileSerializer,
    HostelApplicationSerializer, # Assuming you'll have an Application model/serializer or handle via profile
    ApplicationStatusSerializer,
    PaymentSerializer,
    MaintenanceRequestSerializer,
    HostelCertificateSerializer as StudentHostelCertificateSerializer, # Renamed to avoid conflict if needed
)

# Placeholder Permission Class (will implement logic later)
from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    """Allows access only to users with the 'student' role."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role.name == 'student'

User = get_user_model()

# Placeholder Views (will implement logic later)
class ApplyForHostelView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = HostelApplicationSerializer # Use a serializer that handles profile creation/update

    def post(self, request, *args, **kwargs):
        # Placeholder logic for creating/updating student profile and setting application status
        return Response({'message': 'Apply for Hostel - Placeholder'}, status=status.HTTP_201_CREATED)

class ViewApplicationStatusView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = ApplicationStatusSerializer

    def retrieve(self, request, *args, **kwargs):
        # Placeholder logic to return application status and room details
        return Response({'message': 'View Application Status - Placeholder'}, status=status.HTTP_200_OK)

class StudentProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = StudentProfileSerializer
    queryset = StudentProfile.objects.all()

    def get_object(self):
        return self.request.user.studentprofile

class PayHostelFeeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        # Placeholder logic to create payment entry
        return Response({'message': 'Pay Hostel Fee - Placeholder'}, status=status.HTTP_201_CREATED)

class ViewPaymentHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = PaymentSerializer

    def get_queryset(self):
        # Placeholder logic to return student's payment history
        return Payment.objects.filter(booking__student=self.request.user)

class SubmitMaintenanceRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = MaintenanceRequestSerializer

    def post(self, request, *args, **kwargs):
        # Placeholder logic to create maintenance request
        return Response({'message': 'Submit Maintenance Request - Placeholder'}, status=status.HTTP_201_CREATED)

class ViewMaintenanceRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = MaintenanceRequestSerializer

    def get_queryset(self):
        # Placeholder logic to return student's maintenance requests
        return MaintenanceRequest.objects.filter(submitted_by=self.request.user)

class DownloadHostelCertificateView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = StudentHostelCertificateSerializer # Use a serializer that provides the file link

    def retrieve(self, request, *args, **kwargs):
        # Placeholder logic to return file link if certificate exists and is approved
        return Response({'message': 'Download Hostel Certificate - Placeholder'}, status=status.HTTP_200_OK) 
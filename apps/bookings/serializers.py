from rest_framework import serializers
from .models import Booking, HostelCertificate
from apps.rooms.serializers import RoomSerializer

class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

class HostelCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelCertificate
        fields = '__all__' 
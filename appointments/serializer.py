from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'note', 'status']
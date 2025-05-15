from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, AvailabilitySlot
from core.serializers import DoctorSerializer, PatientSerializer
from user.models import Doctor, Patient
from django.core.exceptions import ValidationError as DjangoValidationError



class AvailabilitySlotSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        source='doctor',
        write_only=True
    )

    class Meta:
        model = AvailabilitySlot
        fields = ['id', 'doctor_id', 'doctor', 'date', 'start_time', 'end_time']

    def validate(self, data):
        instance = AvailabilitySlot(**data)
        
        try:
            instance.full_clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        return data

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(),
        source='patient',
        write_only=True,
    )

    availability_slot = AvailabilitySlotSerializer(read_only=True)
    availability_slot_id = serializers.PrimaryKeyRelatedField(
        queryset = AvailabilitySlot.objects.all(),
        source='availability_slot',
        write_only=True
    )

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_id', 'availability_slot', 'availability_slot_id', 'start_time', 'end_time', 'note', 'status', 'created_at']

    def validate(self, data):
        instance = Appointment(**data)

        try:
            instance.full_clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        return data
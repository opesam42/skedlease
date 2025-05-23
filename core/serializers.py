from rest_framework import serializers
from user.models import Doctor, Patient, Speciality
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'user_role']
        read_only_fields = ['id']

class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialities']
        read_only_fields = ['id']

class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = ['id', 'user', 'matric_number']
        read_only_fields = ['id']

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['id', 'name', 'description']
from django.shortcuts import render
from .serializers import *
from user.models import Doctor
from appointments.models import Appointment
from appointments.serializer import AppointmentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
@api_view(['GET'])
def get_doctors(request):
    doctors = Doctor.objects.all()

    speciality = request.query_params.get('speciality', None)

    if speciality:
        query = Q(speciality__iexact = speciality)
        doctors = doctors.filter(query)
    
    if not doctors.exists():
        return Response(
            {'message': 'No doctor found for this speciality'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializers = DoctorSerializer(doctors, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

@login_required
@api_view(['GET'])
def view_appointments(request):
    appointments = Appointment.objects.all()

    patient = request.query_params.get('patient', None)
    doctor = request.query_params.get('doctor', None)

    if patient:
        query = Q(patient__id = int(patient))
        appointments = appointments.filter(query)
    if doctor:
        query = Q(doctor__id = int(doctor))
        appointments = appointments.filter(query)

    if not appointments.exists():
        return Response(
            {'message': 'No appointments found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializers = AppointmentSerializer(appointments, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
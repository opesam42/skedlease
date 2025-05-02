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


@api_view(['GET'])
def get_doctors(request):
    doctors = Doctor.objects.all()

    speciality = request.query_params.get('speciality', None)

    if speciality:
        query = Q(speciality__iexact = speciality)
        doctors = doctors.filter(query)
    
    if not doctors.exists():
        return Response({
            'message': 'No doctor found for this speciality'
        })

    serializers = DoctorSerializer(doctors, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

# @login_required
@api_view(['GET'])
def view_appointments(request):
    appointments = Appointment.objects.all()
    serializers = AppointmentSerializer(appointments, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
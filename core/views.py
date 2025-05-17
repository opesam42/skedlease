from django.shortcuts import render
from .serializers import *
from user.models import Doctor
from appointments.models import Appointment, AvailabilitySlot
from appointments.serializer import AppointmentSerializer, AvailabilitySlotSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.rolecheck import admin_only
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctors(request):
    doctors = Doctor.objects.all()

    speciality = request.query_params.get('speciality', None)

    if speciality:
        query = Q(specialities__name__iexact = speciality)
        doctors = doctors.filter(query)
    
    if not doctors.exists():
        return Response(
            {'message': 'No doctor found for this speciality'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializers = DoctorSerializer(doctors, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_availabilty_slot(request):
    availability_slots = AvailabilitySlot.objects.all()

    date = request.query_params.get('date', None)
    start_time = request.query_params.get('start_time', None)
    end_time = request.query_params.get('end_time', None)

    if date:
        availability_slots = availability_slots.filter(date = date)

    if start_time and end_time:
        availability_slots = availability_slots.filter(
            start_time__lte=start_time,
            end_time__gte=end_time
    )

    availability_slots = availability_slots.first()
    if not availability_slots:
        return Response(
            {'message': 'No slots found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializers = AvailabilitySlotSerializer(availability_slots)
    return Response(serializers.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def view_appointments(request):
    appointments = Appointment.objects.all()

    patient = request.query_params.get('patient', None)
    doctor = request.query_params.get('doctor', None)
    date = request.query_params.get('date', None)

    if patient:
        appointments = appointments.filter(patient__id = int(patient))
    if doctor:
        appointments = appointments.filter(availability_slot__doctor__id = int(doctor))
    if date:
        appointments = appointments.filter(availability_slot__date=date)

    if not appointments.exists():
        return Response(
            {'message': 'No appointments found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializers = AppointmentSerializer(appointments, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@admin_only
def add_speciality(request):
    serializer = SpecialitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@admin_only
def update_specialities(request, speciality_id):
    try:
        speciality = Speciality.objects.get(id=speciality_id)
    except Speciality.DoesNotExist:
        return Response({"message": "Speciality does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = SpecialitySerializer(speciality, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_specialities(request):
    specialites = Speciality.objects.all()

    serializers = SpecialitySerializer(specialites, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
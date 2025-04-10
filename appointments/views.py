from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import AppointmentSerializer
from .models import Appointment
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
@api_view(['POST'])
def create_appointment(request):
    serializer = AppointmentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

@login_required
@api_view(['PUT'])
def update_appointment(request,id):
    try:
        appointment = Appointment.objects.get(id=id)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AppointmentSerializer(appointment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
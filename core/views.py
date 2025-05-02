from django.shortcuts import render
from .serializers import *
from user.models import Doctor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def get_doctors(request):
    doctors = Doctor.objects.all()
    serializers = DoctorSerializer(doctors, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
from django.shortcuts import render
from django.shortcuts import render
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.rolecheck import admin_only


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@admin_only
def create_speciality(request):
    serializer = SpecialitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
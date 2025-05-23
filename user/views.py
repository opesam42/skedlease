from django.shortcuts import render
from .serializer import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from .models import Patient
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

@api_view(['POST'])
def create_user(request):
    role = request.data.get('user_role')

    if role == 'doctor':
        serializer = DoctorRegistrationSerializer(data=request.data)
    elif role == 'patient':
        serializer = PatientRegistrationSerializer(data=request.data)
    else:
        return Response({'error': 'Invalid or missing user_role. Must be "doctor" or "patient".'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    identifier = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=identifier)
    except User.DoesNotExist:
        try:
            patient = Patient.objects.get(matric_number=identifier)
            user = patient.user
        except Patient.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


    user = authenticate(email=user.email, password=password)
    
    if user:
        login(request, user)

        return Response({
            'message': 'Login successful',
            'user': BaseUserSerializer(user).data,
        })
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})


# Get User Data API (Requires Login)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    return Response(UserDetailSerializer(user).data)

@api_view(['PUT'])
@permission_classes(IsAuthenticated)
def update_user(request):
    user = request.user
    serializer = UserDetailSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# for admin to updte user
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def admin_update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])  # Prevent JWT from blocking it
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({"csrf_token": csrf_token})
from django.shortcuts import render
from .serializer import UserRegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token
# Create your views here.


@api_view(['POST'])
# @permission_classes([AllowAny])  # Prevent JWT from blocking it
def create_user(request):

    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    #in case of validation error
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    email = request.data.get('username')
    password = request.data.get('password')

    print(f"Received email: {email}, password: {password}")

    user = authenticate(email=email, password=password)
    
    if user:
        login(request, user)

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.user_role
            }
        })
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})


# Get User Data API (Requires Login)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_user_data(request):
    return Response({
        'id': request.user.id,
        'email': request.user.email,
        'role': request.user.user_role
    })

@api_view(['GET'])
@permission_classes([AllowAny])  # Prevent JWT from blocking it
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({"csrf_token": csrf_token})
    
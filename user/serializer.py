from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import USER_ROLE_CHOICES, Patient, Doctor

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    user_role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'user_role', 'password', 'password2']

    def validate(self, attrs):
        # to ensure that passwords mathch
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        if attrs['user_role'] == 'patient':
            matric_number = self.initial_data.get('matric_number', None)
            if not matric_number:
                raise serializers.ValidationError({'matric_number': 'This field is required for patients.'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        matric_number = self.initial_data.get('matric_number', None)
        
        user = get_user_model() 
        new_user = user.objects.create_user(**validated_data)

        user_role = validated_data.get('user_role')
        if user_role == "patient":
            Patient.objects.create(user=new_user, matric_number=matric_number)
        elif user_role == "doctor":
            Doctor.objects.create(user=new_user)
            
        return new_user
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import USER_ROLE_CHOICES, Patient, Doctor, Speciality


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    user_role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'user_role', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs

    def create_user(self, validated_data):
        validated_data.pop('password2')
        user_model = get_user_model()
        return user_model.objects.create_user(**validated_data)


class PatientRegistrationSerializer(BaseUserSerializer):
    matric_number = serializers.CharField(write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['matric_number']

    def create(self, validated_data):
        matric_number = validated_data.pop('matric_number')
        validated_data['user_role'] = 'patient'
        user = self.create_user(validated_data)
        Patient.objects.create(user=user, matric_number=matric_number)
        return user


class DoctorRegistrationSerializer(BaseUserSerializer):
    specialities = serializers.PrimaryKeyRelatedField(
        queryset=Speciality.objects.all(), many=True, write_only=True
    )
    
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['specialities']

    def create(self, validated_data):
        specialities = validated_data.pop('specialities')
        validated_data['user_role'] = 'doctor'
        user = self.create_user(validated_data)
        doctor = Doctor.objects.create(user=user)
        doctor.specialities.set(specialities)
        return user




""" 
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
    
class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['id', 'name'] """
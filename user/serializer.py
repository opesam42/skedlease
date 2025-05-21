from rest_framework import serializers
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from .models import USER_ROLE_CHOICES, Patient, Doctor, Speciality
from .generate_password import generate_random_password
from emails.utils import send_doctor_welcome_email

class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    user_role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'user_role', 'password', 'password2']

    def validate(self, attrs):
        if attrs.get('password') and attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs

    def create_user(self, validated_data):
        validated_data.pop('password2', None)
        user_model = get_user_model()
        return user_model.objects.create_user(**validated_data)


class PatientRegistrationSerializer(BaseUserSerializer):
    matric_number = serializers.CharField(write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['matric_number']

    def create(self, validated_data):
        matric_number = validated_data.pop('matric_number')
        validated_data['user_role'] = 'patient'
        
        
        try:
            with transaction.atomic():
                user = self.create_user(validated_data)
                Patient.objects.create(user=user, matric_number=matric_number)
        except IntegrityError as e:
            if 'matric_number' in str(e):
                raise serializers.ValidationError({'matric_number': 'This matric number already exists.'})
            else:
                raise serializers.ValidationError({'non_field_errors': ['There was an issue with the database. Please check your input and try again.']})


        return user


class DoctorRegistrationSerializer(BaseUserSerializer):
    password = 'doctor'
    password2 = 'doctor'

    specialities = serializers.PrimaryKeyRelatedField(
        queryset=Speciality.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta(BaseUserSerializer.Meta):
        base_fields = list(BaseUserSerializer.Meta.fields)
        if 'password' in base_fields:
            base_fields.remove('password')
        if 'password2' in base_fields:
            base_fields.remove('password2')
            
        fields = base_fields + ['specialities']

    def validate_specialities(self, value):
        if value and len(value) > 2:
            raise serializers.ValidationError("A doctor can have at most 2 specialities")
        return value

    def create(self, validated_data):
        specialities = validated_data.pop('specialities', [])
        validated_data['user_role'] = 'doctor'

        generated_password = generate_random_password()
        validated_data['password'] = generated_password
        user = self.create_user(validated_data)
        doctor = Doctor.objects.create(user=user)
        doctor.specialities.set(specialities)

        user.generated_password = generated_password

        # send email
        try:
            send_doctor_welcome_email(user.email, {'doctor': user})
            print(f'Welcome Email sent to Dr. {user.first_name}')
        except Exception as e:
            print(f'Error sending mail', {str(e)})
        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        if hasattr(instance, 'generated_password'):
            data['generated_password'] = instance.generated_password
        return data

class PatientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['matric_number']

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['id', 'name']

class DoctorInfoSerializer(serializers.ModelSerializer):
    specialities = SpecialitySerializer(many=True)

    class Meta:
        model = Doctor
        fields = ['specialities', ]

class UserDetailSerializer(BaseUserSerializer):
    patient_info = serializers.SerializerMethodField()
    doctor_info = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['patient_info', 'doctor_info']

    def get_patient_info(self, obj):
        if obj.user_role == "patient" and hasattr(obj, 'patient'):
            return PatientInfoSerializer(obj.patient).data
        return None
    
    def get_doctor_info(self, obj):
        if obj.user_role == 'doctor' and hasattr(obj, 'doctor'):
            return DoctorInfoSerializer(obj.doctor).data
        return None 
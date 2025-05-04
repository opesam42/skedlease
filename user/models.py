from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from .managers import CustomUserManager

USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
)

# Create your models here.
class CustomUser(AbstractUser):

    username = None #remove username, I want to use email as unique identifier
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False) 
    last_name = models.CharField(max_length=30, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='patient')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Speciality(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Doctor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    specialities = models.ManyToManyField(Speciality, related_name="doctor", blank=False)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class Patient(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=9, unique=True, blank=False, null=True)

    def __str__(self):
        return f"Patient {self.user.first_name} {self.user.last_name}"

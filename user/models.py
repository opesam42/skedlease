from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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
    phone_number = models.CharField(max_length=15)
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='patient')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
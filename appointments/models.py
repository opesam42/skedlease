from django.db import models
from user.models import Doctor, Patient

# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=False, null=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=False, null=False)
    appointment_date = models.DateField(blank=False, null=False)
    appointment_time = models.TimeField(blank=False, null=False)
    note = models.TextField(max_length=500, blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.patient.user.first_name} / Dr. {self.doctor.user.first_name}'
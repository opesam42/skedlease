from rest_framework import serializers
from django.db import models
from django.db.models import Q, F
from user.models import Doctor, Patient
from django.core.exceptions import ValidationError

# Create your models here.


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')
        
        overlapping_slots = AvailabilitySlot.objects.filter(
            doctor = self.doctor,
            date = self.date,
            start_time__lt = self.end_time,
            end_time__gt = self.start_time,
        ).exclude(id=self.id)

        if overlapping_slots.exists():
            raise ValidationError('This availability slot overlaps with an existing one for the same doctor on this date.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}-{self.end_time}"



class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', blank=False, null=False)
    availability_slot = models.ForeignKey(AvailabilitySlot, on_delete=models.CASCADE, related_name='appointments', null=True)
    start_time = models.TimeField(blank=False, null=True)
    end_time = models.TimeField(blank=False, null=True)
    note = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def clean(self):
        slot = self.availability_slot

        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')
        if self.start_time < slot.start_time or self.end_time > slot.end_time:
            raise ValidationError('Appointment time must be within the availability slot\'s time range.')
        
        overlapping_appointments = Appointment.objects.filter(
            availability_slot = self.availability_slot,
            start_time__lt = self.end_time,
            end_time__gt = self.start_time,
        ).exclude(id=self.id)

        if overlapping_appointments.exists():
            raise ValidationError('This appointment overlaps with an existing appointment in the same availability slot.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.patient.user.first_name} / Dr. {self.availability_slot.doctor.user.first_name} - {self.availability_slot.date}. {self.start_time} - {self.end_time}'

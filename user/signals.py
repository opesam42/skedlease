from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient, Doctor
from emails.utils import send_patient_welcome_email, send_doctor_welcome_email

@receiver(post_save, sender=Patient)
def handle_patient_created(sender, instance, created, **kwargs):
    if created:
        send_patient_welcome_email(instance.user.email, {'user': instance.user})
        print(f'Welcome Email sent to {instance.user.first_name}')
# Generated by Django 5.1.7 on 2025-05-15 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_remove_appointment_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='date',
        ),
    ]

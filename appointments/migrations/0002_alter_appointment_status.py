# Generated by Django 5.1.7 on 2025-04-10 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]

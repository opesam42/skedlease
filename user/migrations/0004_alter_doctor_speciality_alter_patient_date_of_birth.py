# Generated by Django 5.1.7 on 2025-04-14 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_doctors_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='speciality',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]

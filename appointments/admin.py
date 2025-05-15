from django.contrib import admin
from .models import Appointment, AvailabilitySlot
# Register your models here.
admin.site.register(Appointment)
admin.site.register(AvailabilitySlot)
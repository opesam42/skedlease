from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Speciality)
admin.site.register(Doctor)
admin.site.register(Patient)
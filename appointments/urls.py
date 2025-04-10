from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('create/', views.create_appointment, name='create_appointment'),
    path('update/<int:id>', views.update_appointment, name='update_appointment'),
]
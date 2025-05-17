from django.urls import path
from . import views
from appointments.views import create_availabilty_slot

app_name = "core"

urlpatterns = [
    path('doctors/', views.get_doctors, name='doctor-list'),
    path('appointments/', views.view_appointments, name='appointment-list'),
    path('slots/', views.get_availabilty_slot, name='get-availability-slots'),
    path('get-occupied-time/<str:date>', views.get_occupied_time, name='get-occupied-time'),
    path('add-speciality/', views.add_speciality, name='add-specialities'),
    path('specialities/', views.get_specialities, name='specialities-list'),
    path('update-speciality/<int:speciality_id>', views.update_specialities, name='update-specialities'),

    path('add-slot/', create_availabilty_slot, name='create-availability-slot'),
]

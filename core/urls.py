from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('doctors/', views.get_doctors, name='doctor-list'),
    path('appointments/', views.view_appointments, name='appointment-list'),
    path('add-speciality/', views.add_speciality, name='add-specialities'),
    path('specialities/', views.get_specialities, name='specialities-list'),
    path('update-speciality/<int:speciality_id>', views.update_specialities, name='update-specialities')
]

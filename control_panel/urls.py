from django.urls import path
from . import views

app_name = 'control_panel'

urlpatterns = [
    path('create-speciality/', views.create_speciality, name='create-speciality'),
]
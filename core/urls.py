from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('doctors/', views.get_doctors, name='doctor-list'),
]

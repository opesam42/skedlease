from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.create_user, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.get_user_data, name='get_user_data'),
]
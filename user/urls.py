from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'user'

urlpatterns = [
    path('signup/', views.create_user, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('info/', views.get_user_data, name='get_user_data'),
    path('update/<int:user_id>/', views.admin_update_user, name='admin-update-user'),

    path('get_csrf/', views.get_csrf_token, name='get_csrf_token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
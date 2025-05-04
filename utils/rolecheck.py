from django.shortcuts import render, redirect
from functools import wraps
from rest_framework import status
from rest_framework.response import Response

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Authentication credentials were not provided or are invalid."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.user.user_role != 'admin':
            return Response(
                {"message": "You do not have permission to perform this action. Admin access required."},
                status=status.HTTP_403_FORBIDDEN
            )

        return view_func(request, *args, **kwargs)
    return wrapper
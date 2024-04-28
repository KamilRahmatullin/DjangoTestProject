from django.urls import path
from django.shortcuts import render
from .views import *

app_name = 'account'

urlpatterns = [
    # register user
    path('register/', register_user_view, name='register'),
    path('email_verification/',
         lambda request: render(request, 'account/email/email_verification.html'),
         name='email_verification'),
]

# upur zvyp mrlw cleg
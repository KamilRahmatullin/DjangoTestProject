from django.urls import path
from django.shortcuts import render
from .views import register_user_view, login_user_view, logout_user_view, dashboard_view, profile_view, \
    delete_users_view

app_name = 'account'

urlpatterns = [
    # register user
    path('register/', register_user_view, name='register'),
    path('email_verification/',
         lambda request: render(request, 'account/email/email_verification.html'),
         name='email_verification'),

    # login user
    path('login/', login_user_view, name='login'),
    path('logout/', logout_user_view, name='logout'),

    # dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile-management/', profile_view, name='profile_management'),
    path('delete-users/', delete_users_view, name='delete_user'),
]

# upur zvyp mrlw cleg

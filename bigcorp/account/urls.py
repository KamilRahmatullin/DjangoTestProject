from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
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

    # password reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password/password_reset.html',
             email_template_name='account/password/password_reset_email.html',
             success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password/password_reset_confirm.html',
             success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password_reset_complete.html'),
         name='password_reset_complete'),
]



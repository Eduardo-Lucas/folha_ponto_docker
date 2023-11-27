"""Module providing a function pathing python version."""
from django.urls import path
from django.urls.base import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import sign_in, logout_view, change_password

app_name = "user"

urlpatterns = [
    path("login/", sign_in, name="login"), # type: ignore
    path("logout/", logout_view, name="logout"),
    path('password-reset/',
         PasswordResetView.as_view(
             success_url=reverse_lazy('user:password_reset_done'),
             template_name='registration/password_reset.html'
        ),
         name='password-reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
        ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
        ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
        ),
         name='password_reset_complete'),
    path("change-password/", change_password, name="change_password"),
]

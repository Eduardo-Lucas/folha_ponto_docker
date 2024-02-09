"""Module providing a function pathing python version."""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView, sign_in, logout_view, success_password

app_name = "user"

urlpatterns = [
    path("login/", sign_in, name="login"),  # type: ignore
    path("logout/", logout_view, name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "password/",
        PasswordsChangeView.as_view(template_name="registration/change_password.html"),
        name="password",
    ),
    path("success_password/", success_password, name="success_password"),
]

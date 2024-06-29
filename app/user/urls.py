"""Module providing a function pathing python version."""

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    AtualizaPerfil,
    PasswordsChangeView,
    ProfileUpdateView,
    logout_view,
    sign_in,
    success_password,
    usuario_autocomplete,
)

app_name = "user"

urlpatterns = [
    path("login/", sign_in, name="login"),  # type: ignore
    path("logout/", logout_view, name="logout"),



    path(
        "password/",
        PasswordsChangeView.as_view(template_name="registration/change_password.html"),
        name="password",
    ),
    path("success_password/", success_password, name="success_password"),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
    path("atualiza_perfil/<int:pk>", AtualizaPerfil.as_view(), name="atualiza_perfil"),
    path("usuario_autocomplete/", usuario_autocomplete, name="usuario_autocomplete"),
]

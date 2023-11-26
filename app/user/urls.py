from django.urls import path
from .views import sign_in, logout_view

app_name = "user"

urlpatterns = [
    path("login/", sign_in, name="login"),
    path("logout/", logout_view, name="logout"),
]

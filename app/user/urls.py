from django.urls import path
from .views import NewLoginView, logout_view

app_name = "user"

urlpatterns = [
    path("login/", NewLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]

from django.urls import path

from . import views

app_name = "cliente"

urlpatterns = [
    path(
        "cliente_autocomplete/", views.cliente_autocomplete, name="cliente_autocomplete"
    ),
]

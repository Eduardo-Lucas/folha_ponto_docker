from django.urls import path, register_converter

from .converters.custom_date_converter import DateConverter
from .views import (
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    apontamento_list,
    folha_ponto,
    mudar_tarefa,
)

app_name = "apontamento"

register_converter(DateConverter, "date")

urlpatterns = [
    path("apontamento-list", apontamento_list, name="apontamento_list"),
    path("folha-ponto", folha_ponto, name="folha_ponto"),
    path(
        "appointment-list/<date:day>/<int:user_id>/",
        AppointmentListView.as_view(),
        name="appointment_list",
    ),
    path(
        "appointment-delete/<int:pk>/",
        AppointmentDeleteView.as_view(),
        name="appointment_delete",
    ),
    path(
        "appointment-update/<int:pk>/",
        AppointmentUpdateView.as_view(),
        name="appointment_update",
    ),
    path(
        "appointment-detail/<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment_detail",
    ),
    path(
        "appointment-create/",
        AppointmentCreateView.as_view(),
        name="appointment_create",
    ),
    path("mudar_tarefa", mudar_tarefa, name="mudar_tarefa"),
]

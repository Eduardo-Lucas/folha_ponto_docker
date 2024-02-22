from django.urls import path, register_converter

from .converters.custom_date_converter import DateConverter

from .views import (
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    HistoricoListView,
    MudarTarefaUpdateView,
    ajuste_ponto,
    apontamento_list,
    fecha_tarefa,
    folha_ponto,
    folha_ponto_sem_form,
    get_30_min_break_list,
    historico_com_datas,
    historico_com_usuario,
    historico_sem_form,
    open_task_list,
    over_10_hour_validation,
    over_10_hours_list,
)

app_name = "apontamento"

register_converter(DateConverter, "date")

urlpatterns = [
    path("apontamento-list", apontamento_list, name="apontamento_list"),
    path("folha-ponto", folha_ponto, name="folha_ponto"),
    path(
        "folha_ponto_sem_form/<date:data_inicial>/<date:data_final>/<int:user_id>/",
        folha_ponto_sem_form,
        name="folha_ponto_sem_form",
    ),
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
    path("mudar_tarefa/<int:pk>", MudarTarefaUpdateView.as_view(), name="mudar_tarefa"),
    path("fecha_tarefa/<int:pk>", fecha_tarefa, name="fecha_tarefa"),
    path("historico/", HistoricoListView.as_view(), name="historico"),
    path("historico_com_usuario/", historico_com_usuario, name="historico_com_usuario"),
    path(
        "historico_com_datas/<date:data_inicial>/<date:data_final>/<int:user_id>",
        historico_com_datas,
        name="historico_com_datas",
    ),
    path(
        "historico_sem_form/<int:user_id>",
        historico_sem_form,
        name="historico_sem_form",
    ),
    path("ajuste_ponto/", ajuste_ponto, name="ajuste_ponto"),
    # Reports
    path("get_30_min_break_list", get_30_min_break_list, name="get_30_min_break_list"),
    path("over_10_hours_list/", over_10_hours_list, name="over_10_hours_list"),
    path(
        "over_10_hour_validation/<date:day>/<int:user_id>",
        over_10_hour_validation,
        name="over_10_hour_validation",
    ),
    path("open_task_list", open_task_list, name="open_task_list"),
]

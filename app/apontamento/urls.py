from django.urls import path, register_converter

from .converters.custom_date_converter import DateConverter
from .views import (
    AjustePontoDetailView,
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    ConsultaUsuarioClienteTarefa,
    HistoricoListView,
    MudarTarefaUpdateView,
    ajuste_ponto,
    apontamento_list,
    autoriza_ajuste,
    autoriza_todos_ajustes,
    recusa_ajuste,
    recusa_todos_ajustes,
    fecha_tarefa,
    fechar_todas_tarefas,
    folha_ponto,
    folha_ponto_sem_form,
    get_30_min_break_list,
    get_automatically_closed_tasks,
    historico_com_datas,
    historico_com_usuario,
    historico_sem_form,
    open_task_list,
    over_10_hour_validation,
    over_10_hours_list,
    get_ajustes_pendentes,
    get_ajustes_nao_autorizados,
    get_ajustes_autorizados,
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
    path("fechar_todas_tarefas", fechar_todas_tarefas, name="fechar_todas_tarefas"),
    path(
        "tarefas_fechadas_automaticamente",
        get_automatically_closed_tasks,
        name="tarefas_fechadas_automaticamente",
    ),
    path(
        "ajustes-pendentes",
        get_ajustes_pendentes,
        name="ajustes_pendentes",
    ),
    path(
        "ajustes-nao-autorizados",
        get_ajustes_nao_autorizados,
        name="ajustes_nao_autorizados",
    ),
    path(
        "ajustes-autorizados",
        get_ajustes_autorizados,
        name="ajustes_autorizados",
    ),
    path(
        "ajuste_ponto_detail/<int:pk>/",
        AjustePontoDetailView.as_view(),
        name="ajuste_ponto_detail",
    ),
    path("autoriza_ajuste/<int:pk>/", autoriza_ajuste, name="autoriza_ajuste"),
    path(
        "autoriza_todos_ajustes/",
        autoriza_todos_ajustes,
        name="autoriza_todos_ajustes",
    ),
    path("recusa_ajuste/<int:pk>/", recusa_ajuste, name="recusa_ajuste"),
    path(
        "recusa_todos_ajustes/",
        recusa_todos_ajustes,
        name="recusa_todos_ajustes",
    ),
    path(
        "consulta_por_user_cliente_tarefa/",
        ConsultaUsuarioClienteTarefa.as_view(),
        name="consulta_por_user_cliente_tarefa",
    ),
]

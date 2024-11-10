from django.urls import path

from . import views

app_name = "refeicao"

urlpatterns = [
    path("refeicao_list/", views.refeicao_listview, name="refeicao_list"),
    path(
        "refeicao_create/", views.RefeicaoCreateView.as_view(), name="refeicao_create"
    ),
    path(
        "refeicao_update/<int:pk>/",
        views.RefeicaoUpdateView.as_view(),
        name="refeicao_update",
    ),
    path(
        "refeicao_delete/<int:pk>/",
        views.RefeicaoDeleteView.as_view(),
        name="refeicao_delete",
    ),
    path(
        "refeicao_detail/<int:pk>/",
        views.RefeicaoDetailView.as_view(),
        name="refeicao_detail",
    ),
    path(
        "user_activity_report/",
        views.user_activity_report,
        name="user_activity_report",
    ),
    path(
        "monthly_report_view/",
        views.MonthlyReportView.as_view(),
        name="monthly_report_view",
    ),

]

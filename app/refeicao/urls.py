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
        "search_refeicao_results/",
        views.SearchRefeicaoResultsView.as_view(),
        name="search_refeicao_results",
    ),
]

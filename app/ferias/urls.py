from django.urls import path

from . import views

app_name = "ferias"

urlpatterns = [
    path("ferias_list/", views.FeriasListView.as_view(), name="ferias_list"),
    path("ferias_create/", views.FeriasCreateView.as_view(), name="ferias_create"),
    path(
        "ferias_update/<int:pk>/",
        views.FeriasUpdateView.as_view(),
        name="ferias_update",
    ),
    path(
        "ferias_delete/<int:pk>/",
        views.FeriasDeleteView.as_view(),
        name="ferias_delete",
    ),
    path(
        "search_ferias_results/",
        views.SearchFeriasResultsView.as_view(),
        name="search_ferias_results",
    ),
]

from django.urls import path

from . import views

app_name = "cliente"

urlpatterns = [
    path(
        "cliente_autocomplete/", views.cliente_autocomplete, name="cliente_autocomplete",
    ),
    path(
    "cliente-insert/", views.ClienteCreateView.as_view(), name="cliente_insert",
    ),
    path(
        "cliente-list/", views.ClienteListView.as_view(), name="cliente_list",
    ),
    path(
        "cliente-list-inativo/", views.ClienteInativoListView.as_view(), name="cliente_list_inativo",
    ),
    path(
        "cliente-update/<int:pk>/", views.ClienteUpdateView.as_view(), name="cliente_update",
    ),
    path(
        "cliente-tipo-senha-insert/<int:cliente_id>/", views.ClienteTipoSenhaCreateView.as_view(), name="cliente_tipo_senha_insert",
    ),
    path(
        "cliente-tipo-senha-list/<int:cliente_id>/", views.ClienteTipoSenhaListView.as_view(), name="cliente_tipo_senha_list",
    ),
    path(
        "cliente-tipo-senha-update/<int:pk>/", views.ClienteTipoSenhaUpdateView.as_view(), name="cliente_tipo_senha_update",
    ),
    path(
        "cliente-tipo-senha-delete/<int:pk>/", views.ClienteTipoSenhaDeleteView.as_view(), name="cliente_tipo_senha_delete",
    ),
]

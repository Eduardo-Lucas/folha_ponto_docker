from django.urls import path
from .views import (
    BancoDeHorasListView,
    BancoDeHorasUpdateView,
    BancoDeHorasDeleteView,
    ValorInseridoListView,
    ValorInseridoUpdateView,
    ValorInseridoDeleteView,
    ValorInseridoCreateView,
)

app_name = "banco_de_horas"

urlpatterns = [
    path(
        "lista_banco_de_horas/",
        BancoDeHorasListView.as_view(),
        name="lista_banco_de_horas",
    ),
    path(
        "atualiza_banco_de_horas/<int:pk>/",
        BancoDeHorasUpdateView.as_view(),
        name="atualiza_banco_de_horas",
    ),
    path(
        "deleta_banco_de_horas/<int:pk>/",
        BancoDeHorasDeleteView.as_view(),
        name="deleta_banco_de_horas",
    ),
    path("valor_inserido/",
        ValorInseridoListView.as_view(),
        name="valor_inserido",
    ),
    path("atualizar_valor_inserido/<int:pk>/",
         ValorInseridoUpdateView.as_view(),
         name="atualizar_valor_inserido",
    ),
    path("deletar_valor_inserido/<int:pk>/",
         ValorInseridoDeleteView.as_view(),
         name="deletar_valor_inserido",
    ),
    path("adicionar_valor_inserido/",
         ValorInseridoCreateView.as_view(),
         name="adicionar_valor_inserido",)

]

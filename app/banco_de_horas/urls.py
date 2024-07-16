from django.urls import path
from .views import (
    BancoDeHorasListView,
    BancoDeHorasUpdateView,
    calcula_banco_de_horas,
    BancoDeHorasDeleteView,
    verica_banco_de_horas_existente,
)

app_name = "banco_de_horas"

urlpatterns = [
    path('verica_banco_de_horas_existente/<date:periodo_apurado>',
         verica_banco_de_horas_existente,
         name='verica_banco_de_horas_existente'
    ),
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
        "calcula_banco_de_horas/",
        calcula_banco_de_horas,
        name="calcula_banco_de_horas"
    ),
    path(
        "deleta_banco_de_horas/<int:pk>/",
        BancoDeHorasDeleteView.as_view(),
        name="deleta_banco_de_horas",
    ),
]

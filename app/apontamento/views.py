from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apontamento.services import PontoService
from apontamento.forms import FolhaPontoForm
from apontamento.models import Ponto

from datetime import datetime, timedelta, timezone
import pytz

from folha_ponto import settings


@login_required
def apontamento_list(request, login_url="users:login"):
    return render(request, "apontamento/apontamento-list.html", {})


def folha_ponto(request):  
    # get sum  of differences group by date #
    #       
    usuario = User.objects.filter(username="sara").first()
    service = PontoService()

    data_inicial=pytz.timezone(settings.TIME_ZONE).localize(datetime(2023, 9, 1, 0, 0, 0)).strftime("%Y-%m-%d")
    data_final  =pytz.timezone(settings.TIME_ZONE).localize(datetime(2023, 9, 3, 0, 0, 0)).strftime("%Y-%m-%d")

    pontos = service.ponto_list(
        usuario.id,
        data_inicial,
        data_final,
    )

    pontos_sumarizados = []
    horas_trabalhadas = timedelta(0)
    total_horas_trabalhadas = timedelta(0)  # total hours worked across all days
    dia = data_inicial
    for ponto in pontos:
        if ponto.entrada.date() != dia:
            pontos_sumarizados.append(
                {
                    "dia": dia,
                    "horas_trabalhadas": horas_trabalhadas,
                }
            )
            total_horas_trabalhadas += horas_trabalhadas  # add the hours worked for the day to the total
            horas_trabalhadas = timedelta(0)
            dia = ponto.entrada.date()
        horas_trabalhadas += ponto.difference
    total_horas_trabalhadas += horas_trabalhadas  # add the hours worked for the last day to the total
    
    context = {"pontos_sumarizados": pontos_sumarizados, "total_horas_trabalhadas": total_horas_trabalhadas}

    return render(
        request,
        "apontamento/folha-ponto.html",
        context,
    )

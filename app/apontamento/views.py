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
    usuario = User.objects.filter(username="sara").first()
    service = PontoService()
    pontos = service.ponto_list(
        usuario.id,
        data_inicial=pytz.timezone(settings.TIME_ZONE).localize(datetime(2023, 9, 1, 0, 0, 0)),
        data_final  =pytz.timezone(settings.TIME_ZONE).localize(datetime(2023, 9, 22, 0, 0, 0)),
    )

    pontos_sumarizados = []
    horas_trabalhadas = timedelta(0)
    for ponto in pontos:
        dia = ponto.entrada.date()
        if ponto.entrada.date() == dia:
            horas_trabalhadas += ponto.difference
            dia = ponto.entrada.date()
        else:    
            print("DIA", dia, "HORAS TRABALHADAS", horas_trabalhadas)
            dict_ponto = {"dia": dia, "horas_trabalhadas": horas_trabalhadas}
            pontos_sumarizados.append(dict_ponto)
            horas_trabalhadas = timedelta(0)


    nome = usuario.username
    context = {"pontos_sumarizados": pontos_sumarizados, 
               "pontos": pontos, 
               "nome": nome}


    return render(
        request,
        "apontamento/folha-ponto.html",
        context,
    )

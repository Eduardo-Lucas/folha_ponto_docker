from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apontamento.services import PontoService
from apontamento.forms import FolhaPontoForm
from apontamento.models import Ponto

from datetime import datetime, timedelta
from django.db.models import Avg, Count, Min, Sum

@login_required
def apontamento_list(request, login_url="users:login"):
    return render(request, "apontamento/apontamento-list.html", {})


def folha_ponto(request):        
    usuario = User.objects.filter(username="sara").first()
    service = PontoService()
    pontos = service.ponto_list(
        usuario.id,
        data_inicial=datetime(2023, 9, 1, 0, 0, 0).date(),
        data_final=datetime(2023, 9, 2, 0, 0, 0).date(),
    )

    pontos_sumarizados = []
    diferenca = timedelta(0)
    for ponto in pontos:
        dia = ponto.entrada.date()
        if ponto.entrada.date() == dia:
            diferenca += ponto.saida - ponto.entrada
        else:
            diferenca = timedelta(0)
            pontos_sumarizados.append(dia, diferenca)


    nome = usuario.username
    context = {"pontos_sumarizados": pontos_sumarizados, "nome": nome}


    return render(
        request,
        "apontamento/folha-ponto.html",
        context,
    )

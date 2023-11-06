from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apontamento.services import PontoService
from apontamento.forms import FolhaPontoForm
from apontamento.models import Ponto

from datetime import datetime, timedelta


@login_required
def apontamento_list(request, login_url="users:login"):
    return render(request, "apontamento/apontamento-list.html", {})


def folha_ponto(request):
    if request.method == "POST":
        form = FolhaPontoForm(request.POST)
        if form.is_valid():
            usuario = User.objects.filter(username="sara").first()
            service = PontoService()
            
            # get sum  of differences group by date #
            #       
            usuario = User.objects.filter(username="sara").first()
            service = PontoService()

            data_inicial=form.cleaned_data["entrada"]
            data_final  =form.cleaned_data["saida"]

            pontos = service.ponto_list(
                usuario.id,
                data_inicial,
                data_final,
            )

            pontos_sumarizados = []
            horas_trabalhadas = timedelta(0)
            total_horas_trabalhadas = timedelta(0)  # total hours worked across all days
            
            horas_obrigatorias = timedelta(hours=8)  # hours worked per day
            total_credor = timedelta(0)
            total_devedor = timedelta(0)
            dia = data_inicial  # start with the first day in the query

            for ponto in pontos:
                print(ponto.entrada.date(), dia)
                if ponto.entrada.date() != dia:  # if the day has changed since the last time we added a sum for a
                    credor_devedor = (horas_obrigatorias - horas_trabalhadas)
                    if credor_devedor > timedelta(0):
                        credor = timedelta(0)
                        devedor = abs(credor_devedor)
                    else:
                        credor = abs(credor_devedor)
                        devedor = timedelta(0)

                    pontos_sumarizados.append(
                        {
                            "dia": dia,
                            "horas_trabalhadas": horas_trabalhadas,
                            "credor": credor,
                            "devedor": devedor,
                        }
                    )
                    total_horas_trabalhadas += horas_trabalhadas  # add the hours worked for the day to the total
                    total_credor += credor
                    total_devedor += devedor 
                    horas_trabalhadas = timedelta(0)
                    dia = ponto.entrada.date()
                horas_trabalhadas += ponto.difference

            total_horas_trabalhadas += horas_trabalhadas  # add the hours worked for the last day to the total


            context = {"pontos": pontos, 
                    "pontos_sumarizados": pontos_sumarizados, 
                    "horas_trabalhadas": horas_trabalhadas,
                    "total_credor": total_credor,
                    "total_devedor": total_devedor,
                    "total_horas_trabalhadas": total_horas_trabalhadas,
                    }
            return render(request, "apontamento/folha-ponto.html", context)

    
    else:
        form = FolhaPontoForm()
        return render(request, "apontamento/folha-ponto.html", {"form": form})
    
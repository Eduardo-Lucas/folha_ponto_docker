from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apontamento.services import PontoService
from apontamento.forms import FolhaPontoForm
from apontamento.models import Ponto

from django.views.generic import ListView

from django.utils import timezone

@login_required
def apontamento_list(request):
    """Listagem de pontos"""
    return render(request, "apontamento/apontamento-list.html", {})


def folha_ponto(request):
    """Folha de ponto"""
    if request.method == "POST":
        form = FolhaPontoForm(request.POST)
        if form.is_valid():
            usuario = User.objects.filter(username="sara").first()
            service = PontoService()

            # get sum  of differences group by date #
            
            data_inicial=form.cleaned_data["entrada"]
            data_final  =form.cleaned_data["saida"]
            usuario = form.cleaned_data["usuario"]
            
            usuario = User.objects.filter(username=usuario).first()
            
            service = PontoService()

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
            atrasado = 'Não'

            for ponto in pontos:

                if ponto.primeiro:
                    if ponto.entrada.time() > datetime.strptime("09:15:00", "%H:%M:%S").time():
                        atrasado = 'Sim'
                    else:
                        atrasado = 'Não'
                else:
                    atrasado = 'Não'
                    
                # if the day has changed since the last time we added a sum for a day
                if ponto.entrada.date() != dia:
                    if ponto.entrada.weekday() >= 5: # it's a weekend
                        credor = horas_trabalhadas
                        devedor = timedelta(0)
                    else:
                        credor_devedor = horas_obrigatorias - horas_trabalhadas

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
                            "atrasado": atrasado,
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

            total_horas_trabalhadas += horas_trabalhadas
            # add the hours worked for the last day to the total


            context = {
                "form": form,
                "pontos": pontos,
                "pontos_sumarizados": pontos_sumarizados, 
                "horas_trabalhadas": horas_trabalhadas,
                "total_credor": total_credor,
                "total_devedor": total_devedor,
                "total_horas_trabalhadas": total_horas_trabalhadas,
            }
            

    
    else:
        form = FolhaPontoForm()
        context = {
                "form": form,
                "pontos": "",
                "pontos_sumarizados": "", 
                "horas_trabalhadas": "",
                "total_credor": "",
                "total_devedor": "",
                "total_horas_trabalhadas": "",
            }

    return render(request, "apontamento/folha-ponto.html", context)


class AppointmentListView(ListView):
    """
    List all the appointments for a specific date.
    """
    model = Ponto
    template_name = 'apontamento/appointment_list.html'
    form_class = FolhaPontoForm
    context_object_name = 'pontos'

    def get_queryset(self):
        date = timezone.datetime(2023, 9, 1).date()
        user=9
        return Ponto.objects.for_day(date, user)
    
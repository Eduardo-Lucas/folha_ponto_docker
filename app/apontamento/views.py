from datetime import datetime, timedelta
from typing import Any

from apontamento.forms import AppointmentCreateForm, FolhaPontoForm
from apontamento.models import Ponto
from apontamento.services import PontoService
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


def apontamento_list(request):
    """Listagem de pontos"""
    return render(request, "apontamento/apontamento-list.html", {})


def folha_ponto(request):
    """Folha de ponto"""
    context = {}
    if request.method == "POST":
        form = FolhaPontoForm(request.POST)
        if form.is_valid():
            usuario = User.objects.filter(username=request.user).first()
            service = PontoService()

            # get sum  of differences group by date #

            data_inicial = form.cleaned_data["entrada"]
            data_final = form.cleaned_data["saida"]
            usuario = form.cleaned_data["usuario"]

            if data_inicial > data_final:
                messages.error(
                    request, "Data inicial não pode ser maior que data final"
                )

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

            # data_inicial is date
            dia = data_inicial

            atrasado = "Não"

            for ponto in pontos:
                if ponto.primeiro:
                    if (
                        ponto.entrada.time()
                        > datetime.strptime("09:15:00", "%H:%M:%S").time()
                    ):
                        atrasado = "Sim"
                    else:
                        atrasado = "Não"
                else:
                    atrasado = "Não"

                # if the day has changed since the last time we added a sum for a day
                if ponto.entrada.date() != dia:
                    if ponto.entrada.weekday() >= 5:  # it's a weekend
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
                            "usuario": usuario.id,
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
            return render(request, "apontamento/folha-ponto.html", context)
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
    template_name = "apontamento/appointment_list.html"
    context_object_name = "pontos"

    def get_queryset(self):
        day = self.kwargs["day"]
        usuario = self.kwargs["user_id"]
        return Ponto.objects.for_day(day, usuario)

    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        context["day"] = self.kwargs["day"]
        context["user"] = User.objects.get(id=self.kwargs["user_id"])
        context["previous_page"] = self.request.META.get("HTTP_REFERER")
        return context


class AppointmentDeleteView(DeleteView):
    """Delete an appointment."""

    model = Ponto
    success_url = reverse_lazy("core:home")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Appointment deleted successfully")
        return super().delete(request, *args, **kwargs)


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """Create a new appointment."""

    model = Ponto
    form_class = AppointmentCreateForm
    template_name = "apontamento/appointment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["usuario"] = self.request.user
        context["dia"] = timezone.now().date()
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)

        instance.usuario = User.objects.filter(username=self.request.user).first()

        # Check if there is data for that day
        # If not, update the field entrada, otherwise update the field saida

        check = Ponto.objects.filter(
            entrada__date=timezone.now().date(), usuario=instance.usuario
        ).last()
        if check:
            if check.saida is not None:
                # If there is data for that day and saida is informed, update the field entrada
                max_id = Ponto.objects.aggregate(Max("id"))["id__max"]
                instance.id = max_id + 1 if max_id is not None else 1
                instance.entrada = timezone.now().replace(microsecond=0)
                instance.fechado = False
            else:
                # If there is data for that day and saida is not informed, update the field saida
                instance.id = check.id
                instance.entrada = check.entrada
                instance.saida = timezone.now().replace(microsecond=0)
                instance.fechado = True
        else:
            # If there is data for that day and saida is informed, update the field entrada
            max_id = Ponto.objects.aggregate(Max("id"))["id__max"]
            instance.id = max_id + 1 if max_id is not None else 1
            instance.entrada = timezone.now().replace(microsecond=0)
            instance.fechado = False

        instance.save()
        messages.success(self.request, "Appointment created successfully")
        return super().form_valid(form)


class AppointmentUpdateView(UpdateView):
    """
    This view is responsible for handling the update operation for an Appointment instance.
    It uses Django's built-in UpdateView which provides a form on the template for the specified model
    and handles the update operation.
    """

    model = Ponto
    fields = [
        "entrada",
        "saida",
        "atraso",
        "atrasoautorizado",
        "tipo_receita",
        "cliente_id",
    ]
    template_name = "apontamento/appointment_update.html"

    def form_valid(self, form):
        messages.info(self.request, "Appointment updated successfully")
        return super().form_valid(form)


class AppointmentDetailView(DetailView):
    """
    This view is responsible for handling the detail view for an Appointment instance.
    It uses Django's built-in DetailView which provides a form on the template for the specified model
    and handles the detail view.
    """

    model = Ponto
    template_name = "apontamento/appointment_detail.html"
    context_object_name = "ponto"

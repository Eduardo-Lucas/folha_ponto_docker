from datetime import datetime, timedelta
from typing import Any

from apontamento.forms import AjustePontoForm, AppointmentCreateForm, FolhaPontoForm
from apontamento.models import Ponto
from apontamento.services import PontoService
from cliente.models import Cliente
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


@login_required
def apontamento_list(request):
    """Listagem de pontos"""
    return render(request, "apontamento/apontamento-list.html", {})


@login_required
def folha_ponto_copy(request):
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

                # if the day has changed since the last time we added a sum for a day
                if ponto.entrada.date() != dia:

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


class AppointmentListView(LoginRequiredMixin, ListView):
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


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
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
        context["dia"] = datetime.now().date()
        context["fechar_tarefa"] = (
            True
            if Ponto.objects.filter(
                usuario=User.objects.filter(username=self.request.user).first(),
                entrada__year__gte=2024,
                saida=None,
            ).last()
            else False
        )
        return context

    def form_valid(self, form):
        # check if tipo_receita is Ativo
        if form.cleaned_data["tipo_receita"].status == "Inativo":
            messages.error(self.request, "Tipo de Receita cannot be Inativo.")
            return super().form_invalid(form)

        if form.cleaned_data["cliente"] is None:
            messages.error(self.request, "Cliente cannot be empty.")
            return super().form_invalid(form)

        instance = form.save(commit=False)

        # turn cliente_id text into id
        # check if there is | in cliente_id
        if "|" in form.cleaned_data["cliente"]:
            instance.cliente_id = Cliente.objects.filter(
                codigosistema=int(form.cleaned_data["cliente"].split("|")[0]),
                nomerazao=form.cleaned_data["cliente"].split("|")[1],
            ).first()
        else:
            instance.cliente_id = Cliente.objects.filter(
                nomerazao=form.cleaned_data["cliente"]
            ).first()

        if not instance.cliente_id:
            messages.error(
                self.request,
                f"Cliente não encontrado: {form.cleaned_data['cliente']}",
            )
            return super().form_invalid(form)

        instance.usuario = User.objects.filter(username=self.request.user).first()

        # Check if there is data for that day
        # If not, update the field entrada, otherwise update the field saida

        check = Ponto.objects.filter(
            entrada__date=datetime.now().date(), usuario=instance.usuario
        ).last()
        if check:
            if check.saida is not None:
                # If there is data for that day and saida is informed, update the field entrada
                max_id = Ponto.objects.aggregate(Max("id"))["id__max"]
                instance.id = max_id + 1 if max_id is not None else 1
                instance.entrada = datetime.now().replace(microsecond=0)
                instance.fechado = False
            else:
                # If there is data for that day and saida is not informed, update the field saida
                instance.id = check.id
                instance.entrada = check.entrada
                instance.saida = datetime.now().replace(microsecond=0)
                instance.fechado = True
        else:
            # If there is data for that day and saida is informed, update the field entrada
            max_id = Ponto.objects.aggregate(Max("id"))["id__max"]
            instance.id = max_id + 1 if max_id is not None else 1
            instance.entrada = datetime.now().replace(microsecond=0)
            instance.fechado = False

        instance.save()
        messages.success(self.request, "Appointment created successfully")
        return super().form_valid(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
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
        # get the new values from the form
        new_entrada = form.cleaned_data["entrada"]
        new_saida = form.cleaned_data.get(
            "saida"
        )  # replace "saida" with the actual field name if it's different

        # get the old values from the database
        old_entrada = self.object.entrada
        old_saida = (
            self.object.saida
        )  # replace "saida" with the actual field name if it's different

        # check if the values were updated
        if new_entrada == old_entrada and new_saida == old_saida:
            messages.info(self.request, "Appointment updated successfully")
            return super().form_valid(form)
        else:
            # get the value of saida in form
            entrada = form.cleaned_data["entrada"]

            # get all the data from saida
            day = entrada.date()
            pontos = Ponto.objects.for_day(day, self.request.user)
            # check if saida surpass any previous saida and not already updated
            for ponto in pontos:
                if ponto.entrada is not None:
                    if entrada > ponto.entrada:
                        messages.error(
                            self.request,
                            f"Entrada cannot be greater than {ponto.id}|{ponto.entrada.strftime('%H:%M:%S')}",
                        )
                        entrada = None
                        return super().form_invalid(form)


class AppointmentDetailView(LoginRequiredMixin, DetailView, UpdateView):
    """
    This view is responsible for handling the detail view for an Appointment instance.
    It uses Django's built-in DetailView which provides a form on the template for the specified model
    and handles the detail view.
    """

    def get_context_data(self, **kwargs):
        context = super(AppointmentDetailView, self).get_context_data(**kwargs)
        context["historico"] = Ponto.objects.for_day(
            self.object.entrada.date(), self.object.usuario
        )
        context["total_trabalhado"] = Ponto.objects.total_day_time(
            self.object.entrada.date(), self.object.usuario
        )
        context["fechar_tarefa"] = (
            True
            if Ponto.objects.filter(
                usuario=User.objects.filter(username=self.request.user).first(),
                entrada__year__gte=2024,
                saida=None,
            ).last()
            else False
        )
        context["data_de_hoje"] = datetime.now().date()
        return context

    model = Ponto
    template_name = "apontamento/appointment_detail.html"
    context_object_name = "ponto"
    fields = [
        "saida",
    ]

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Ponto, pk=self.kwargs["pk"])

    def form_valid(self, form):
        """Muda a tarefa do último ponto do usuário"""

        if not form.cleaned_data["saida"]:
            form.cleaned_data["saida"] = datetime.now().replace(microsecond=0)

            messages.info(
                self.request,
                "The last appointment was updated and closed.",
            )
        return reverse("apontamento:appointment_create")


class MudarTarefaUpdateView(LoginRequiredMixin, UpdateView):
    """Muda a tarefa do último ponto do usuário"""

    model = Ponto
    fields = [
        "saida",
    ]

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return get_object_or_404(Ponto, pk=self.kwargs["pk"])

    def form_valid(self, form):
        """Muda a tarefa do último ponto do usuário"""

        if not form.cleaned_data["saida"]:
            form.cleaned_data["saida"] = datetime.now().replace(microsecond=0)

            messages.info(
                self.request,
                "The last appointment was updated and closed.",
            )
        return reverse("apontamento:appointment_create")


class HistoricoListView(LoginRequiredMixin, ListView):
    """Detalhe do histórico"""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(HistoricoListView, self).get_context_data(**kwargs)
        context["historico"] = Ponto.objects.for_day(
            datetime.now().date(), self.request.user
        )
        context["total_trabalhado"] = Ponto.objects.total_day_time(
            datetime.now().date(), self.request.user
        )
        context["fechar_tarefa"] = (
            True
            if Ponto.objects.filter(
                usuario=User.objects.filter(username=self.request.user).first(),
                entrada__year__gte=2024,
                saida=None,
            ).last()
            else False
        )
        context["data_de_hoje"] = datetime.now().date()

        return context

    model = Ponto
    template_name = "apontamento/appointment_detail.html"
    context_object_name = "ponto"


def fecha_tarefa(request, pk):
    """Fecha a tarefa do último ponto do usuário"""

    ponto = get_object_or_404(Ponto, pk=pk)
    ponto.saida = datetime.now().replace(microsecond=0)
    ponto.fechado = True
    ponto.save()
    messages.info(request, "The last appointment was closed.")
    return redirect("apontamento:appointment_create")


def folha_ponto(request):
    """Retorna o total de horas trabalhadas em um intervalo de datas"""
    form = FolhaPontoForm(user=request.user)
    context = {
        "form": form,
    }
    if request.method == "POST":
        form = FolhaPontoForm(request.POST)
        if form.is_valid():
            data_inicial = form.cleaned_data["entrada"]
            data_final = form.cleaned_data["saida"]
            usuario = form.cleaned_data["usuario"]

            if data_inicial > data_final:
                messages.error(
                    request, "Data inicial não pode ser maior que data final"
                )

        query = Ponto.objects.get_total_hours_by_day_by_user(
            start=data_inicial, end=data_final, user=usuario
        )

        dict_total_credor_devedor = Ponto.objects.get_credor_devedor(
            start=data_inicial, end=data_final, user=usuario
        )

        context = {
            "form": form,
            "query": query,
            "total_trabalhado": Ponto.objects.total_range_days_time(
                data_inicial, data_final, usuario
            ),
            "total_credor": dict_total_credor_devedor["total_credor"],
            "total_devedor": dict_total_credor_devedor["total_devedor"],
            "usuario_id": User.objects.filter(username=request.user).first().id,
        }
    return render(request, "apontamento/folha-ponto.html", context)


def historico_com_usuario(request):
    """Retorna o histórico de um usuário"""
    form = FolhaPontoForm(user=request.user)
    context = {
        "form": form,
    }
    if request.method == "POST":
        form = FolhaPontoForm(request.POST)
        if form.is_valid():
            data_inicial = form.cleaned_data["entrada"]
            data_final = form.cleaned_data["saida"]
            usuario = form.cleaned_data["usuario"]

            if data_inicial > data_final:
                messages.error(
                    request, "Data inicial não pode ser maior que data final"
                )
        historico = Ponto.objects.for_range_days(data_inicial, data_final, usuario)

        context = {
            "form": form,
            "historico": historico,
            "total_trabalhado": Ponto.objects.total_range_days_time(
                data_inicial, data_final, usuario
            ),
        }
    return render(request, "apontamento/historico_com_usuario.html", context)


def over_10_hours_list(request):
    """Listagem de pontos com mais de 10 horas"""
    pontos = Ponto.objects.get_over_10_hours_list()
    context = {
        "pontos": pontos,
    }
    return render(request, "apontamento/over_10_hours_list.html", context)


def get_30_min_break_list(request):
    """Listagem de pontos sem intervalo de 30 minutos"""
    pontos = Ponto.objects.get_30_min_break_list()
    context = {
        "pontos": pontos,
    }
    return render(request, "apontamento/30_min_break_list.html", context)


@login_required
def ajuste_ponto(request):
    """Ajuste de ponto"""

    form = AjustePontoForm()
    context = {
        "form": form,
    }
    if request.method == "POST":
        form = AjustePontoForm(request.POST)

        if form.is_valid():
            entrada = form.cleaned_data["entrada"]
            saida = form.cleaned_data["saida"]
            tipo_receita = form.cleaned_data["tipo_receita"]

            usuario = User.objects.filter(username=request.user).first()

            if entrada > saida:
                # raise validation error
                messages.error(request, "Entrada cannot be greater than saida")

            # turn cliente_id text into id
            # check if there is | in cliente_id
            cliente_id = form.cleaned_data.get("cliente_id")
            if cliente_id and "|" in "cliente_id":
                cliente_id = Cliente.objects.filter(
                    codigosistema=int(form.cleaned_data["cliente_id"].split("|")[0]),
                    nomerazao=form.cleaned_data["cliente_id"].split("|")[1],
                ).first()
            else:
                cliente_id = Cliente.objects.filter(
                    nomerazao=form.cleaned_data["cliente_id"]
                ).first()

            max_id = Ponto.objects.aggregate(Max("id"))["id__max"]
            Ponto.objects.create(
                id=max_id + 1,
                entrada=entrada,
                saida=saida,
                tipo_receita=tipo_receita,
                cliente_id=cliente_id,
                usuario=usuario,
            )
            messages.success(request, "Appointment created successfully")
        else:
            # get the validatin error message
            messages.error(request, form.errors.as_text())

    return render(request, "apontamento/ajuste_ponto.html", context)

from datetime import datetime
from typing import Any

from apontamento.forms import AjustePontoForm, AppointmentCreateForm, FolhaPontoForm
from apontamento.models import Ponto
from cliente.models import Cliente
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

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
        messages.success(self.request, "O ponto foi marcado com sucesso!")
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

    # def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
    #     return get_object_or_404(Ponto, pk=self.kwargs["pk"])

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

    # def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
    #     return get_object_or_404(Ponto, pk=self.kwargs["pk"])

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


@login_required
def fecha_tarefa(request, pk):
    """Fecha a tarefa do último ponto do usuário
    Se usuario for o dono da tarefa OU se o usuario for superuser
    """

    ponto = get_object_or_404(Ponto, pk=pk)

    if ponto.usuario == request.user or request.user.is_superuser:

        if ponto.entrada.date() == datetime.now().date():
            ponto.saida = datetime.now().replace(microsecond=0)
        else:
            ponto.saida = ponto.entrada.replace(hour=23, minute=59, second=59)

        ponto.saida = datetime.now().replace(microsecond=0)
        ponto.fechado = True
        ponto.save()
        messages.info(request, "A tarefa foi fechada.")
        return redirect("apontamento:appointment_create")

    else:
        messages.error(
            request,
            f"Olá {request.user}! Você não tem permissão para fechar a tarefa de {ponto.usuario}.",
        )
        return redirect("core:home")


@login_required
def folha_ponto(request):
    """Retorna o total de horas trabalhadas em um intervalo de datas"""
    form = FolhaPontoForm(user=request.user)
    context = {
        "form": form,
    }
    if request.method == "POST":
        form = FolhaPontoForm(request.POST)
        if form.is_valid():

            data_inicial = str(form.cleaned_data["entrada"])
            data_final = str(form.cleaned_data["saida"])
            usuario = form.cleaned_data["usuario"]
            user = User.objects.filter(username=usuario).first()

            if data_inicial > data_final:
                messages.error(
                    request, "Data inicial não pode ser maior que data final"
                )

        query = Ponto.objects.get_total_hours_by_day_by_user(
            start=data_inicial, end=data_final, user=user
        )

        dict_total_credor_devedor = Ponto.objects.get_credor_devedor(
            start=data_inicial, end=data_final, user=user
        )

        total_credor = dict_total_credor_devedor["total_credor"]
        total_devedor = dict_total_credor_devedor["total_devedor"]
        saldo = (
            total_credor - total_devedor
            if total_credor > total_devedor
            else total_devedor - total_credor
        )

        context = {
            "form": form,
            "query": query,
            "total_trabalhado": Ponto.objects.total_range_days_time(
                data_inicial, data_final, usuario
            ),
            "total_credor": total_credor,
            "total_devedor": total_devedor,
            "saldo": saldo,
            "usuario_id": user.id,
        }
    return render(request, "apontamento/folha-ponto.html", context)


@login_required
def folha_ponto_sem_form(request, data_inicial, data_final, user_id):
    """Retorna o total de horas trabalhadas em um intervalo de datas"""

    usuario = User.objects.get(id=user_id)

    if data_inicial > data_final:
        messages.error(request, "Data inicial não pode ser maior que data final")

    query = Ponto.objects.get_total_hours_by_day_by_user(
        start=data_inicial, end=data_final, user=usuario
    )

    dict_total_credor_devedor = Ponto.objects.get_credor_devedor(
        start=data_inicial, end=data_final, user=usuario
    )

    context = {
        "query": query,
        "total_trabalhado": Ponto.objects.total_range_days_time(
            data_inicial, data_final, usuario
        ),
        "usuario": usuario,
        "total_credor": dict_total_credor_devedor["total_credor"],
        "total_devedor": dict_total_credor_devedor["total_devedor"],
    }

    return render(request, "apontamento/folha-ponto_sem_form.html", context)


@login_required
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


@login_required
def historico_com_datas(request, data_inicial, data_final, user_id):
    """Retorna o histórico de um usuário"""

    # Access variables from session
    data_inicial = (
        request.session.get("data_inicial") if data_inicial is None else data_inicial
    )
    data_final = request.session.get("data_final") if data_final is None else data_final

    if data_inicial > data_final:
        messages.error(request, "Data inicial não pode ser maior que data final")

    usuario = User.objects.get(id=user_id)

    data_inicial = data_inicial.strftime("%Y-%m-%d")
    data_final = data_final.strftime("%Y-%m-%d")

    historico = Ponto.objects.for_range_days(data_inicial, data_final, user_id)

    context = {
        "usuario": usuario,
        "historico": historico,
        "total_trabalhado": Ponto.objects.total_range_days_time(
            data_inicial, data_final, user_id
        ),
    }
    return render(request, "apontamento/historico_sem_form.html", context)


@login_required
def historico_sem_form(request, user_id):
    """Retorna o histórico de um usuário"""

    # Access variables from session
    data_inicial = request.session.get("data_inicial")
    data_final = request.session.get("data_final")

    if data_inicial > data_final:
        messages.error(request, "Data inicial não pode ser maior que data final")

    usuario = User.objects.get(id=user_id)

    historico = Ponto.objects.for_range_days(data_inicial, data_final, user_id)

    context = {
        "usuario": usuario,
        "historico": historico,
        "total_trabalhado": Ponto.objects.total_range_days_time(
            data_inicial, data_final, user_id
        ),
    }
    return render(request, "apontamento/historico_sem_form.html", context)


@login_required
def over_10_hours_list(request):
    """Listagem de pontos com mais de 10 horas"""
    pontos = Ponto.objects.get_over_10_hours_list()
    context = {
        "pontos": pontos,
    }
    return render(request, "apontamento/over_10_hours_list.html", context)


@login_required
def over_10_hour_validation(request, day, user_id):
    """Validação de ponto com mais de 10 horas"""

    data_inicial = day.strftime("%Y-%m-%d")
    data_final = data_inicial

    usuario = User.objects.get(id=user_id)

    pontos = Ponto.objects.for_range_days(data_inicial, data_final, user_id)
    if pontos.exists():
        for ponto in pontos:
            ponto.over_10_hours_authorization = True
            ponto.save()
        dia = day.strftime("%d/%m/%Y")
        messages.info(
            request,
            f"Os registros de Ponto que somam mais de 10 horas do usuário \
                {usuario.username.capitalize()} do dia \
                    {dia} foram autorizados!",
        )

    return redirect("apontamento:over_10_hours_list")


@login_required
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
                ajuste=True,
                ajuste_autorizado=False,
            )
            messages.success(request, "Appointment created successfully")
        else:
            # get the validatin error message
            messages.error(request, form.errors.as_text())

    return render(request, "apontamento/ajuste_ponto.html", context)


@login_required
def open_task_list(request):
    """Listagem de tarefas abertas"""
    pontos = Ponto.objects.get_open_task_list()
    context = {
        "pontos": pontos,
    }
    return render(request, "apontamento/open_task_list.html", context)


@login_required
def fechar_todas_tarefas(request):
    """Fecha todas as tarefas abertas"""
    pontos = Ponto.objects.get_open_task_list()
    for ponto in pontos:
        ponto_obj = Ponto.objects.get(id=ponto["ponto_id"])
        ponto_obj.saida = ponto["entrada"].replace(hour=23, minute=59, second=59)
        ponto_obj.fechado = True
        ponto_obj.save()
    messages.info(request, "Todas as tarefas foram fechadas.")
    return redirect(to="apontamento:open_task_list")


@login_required
def get_automatically_closed_tasks(request):
    """Get all tasks that were automatically closed"""
    pontos_list = Ponto.objects.get_automatically_closed_tasks().order_by("-id")
    paginator = Paginator(pontos_list, 10)

    page_number = request.GET.get("page")
    pontos = paginator.get_page(page_number)

    return render(
        request, "apontamento/tarefas_fechadas_automaticamente.html", {"pontos": pontos}
    )

@login_required
def get_ajustes_nao_autorizados(request):
    """Get all tasks that were not authorized"""
    pontos_list = Ponto.objects.get_ajustes_nao_autorizados().order_by("-id")
    paginator = Paginator(pontos_list, 10)

    page_number = request.GET.get("page")
    pontos = paginator.get_page(page_number)

    return render(
        request, "apontamento/ajustes_nao_autorizados.html", {"pontos_list": pontos_list}
    )


class AjustePontoDetailView(LoginRequiredMixin, DetailView):
    """Detalhe do ajuste de ponto"""

    model = Ponto
    template_name = "apontamento/ajuste_ponto_detail.html"
    success_url = reverse_lazy("apontamento:ajustes_nao_autorizados")
    context_object_name = "ponto"

def autoriza_ajuste(request, pk):
    """Autoriza ajuste de ponto"""
    ponto = get_object_or_404(Ponto, pk=pk)
    ponto.ajuste_autorizado = True
    ponto.save()
    messages.info(request, "Ajuste de ponto autorizado.")
    return redirect("apontamento:ajustes_nao_autorizados")

def autoriza_todos_ajustes(request):
    """Autoriza todos os ajustes de ponto"""
    pontos = Ponto.objects.get_ajustes_nao_autorizados()
    for ponto in pontos:
        ponto_obj = Ponto.objects.get(id=ponto["ponto_id"])
        ponto_obj.ajuste_autorizado = True
        ponto_obj.save()
    messages.info(request, "Todos os ajustes de ponto foram autorizados.")
    return redirect("apontamento:ajustes_nao_autorizados")

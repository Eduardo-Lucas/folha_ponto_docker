"""Views do app banco_de_horas."""

from datetime import datetime, timedelta

from apontamento.models import Ponto
from banco_de_horas.forms import BancoDeHorasForm
from banco_de_horas.models import BancoDeHoras
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from .forms import BancoDeHorasForm, SearchFilterForm

import calendar

def calcula_banco_de_horas(request):
    """Calcula o saldo de horas do usuário."""

    # pega todos usuarios ativos
    users = User.objects.filter(
        is_active=True,
        userprofile__isnull=False,
    )

    # pega o periodo de apuração
    data_inicial = "2024-06-01"
    data_final = "2024-06-30"

    # cast data_final into datetime
    data_final_object = datetime.strptime(data_final, "%Y-%m-%d")

    # periodo anterios é o ultimo dia do mês anterior
    data_anterior = "2024-05-31"

    # remover todas horas
    BancoDeHoras.objects.remover_todas_horas(periodo=data_final)

    # para cada usuario, calcula o saldo de horas
    for user in users:

        saldo_anterior = BancoDeHoras.objects.consultar_saldo(
            user_id=user.id, periodo=data_anterior
        )

        dict_total_credor_devedor = Ponto.objects.get_credor_devedor(
            start=data_inicial, end=data_final, user=user
        )
        total_credor = dict_total_credor_devedor["total_credor"]
        total_devedor = dict_total_credor_devedor["total_devedor"]

        # salva o saldo de horas no banco de horas
        BancoDeHoras.objects.create(
            user=user,
            periodo_apurado=data_final,
            saldo_anterior=saldo_anterior,
            total_credor=total_credor,
            compensacao=timedelta(hours=0, minutes=0, seconds=0),
            total_devedor=total_devedor,
        )

        # lista o banco de horas do periodo
        banco_de_horas = BancoDeHoras.objects.filter(
            periodo_apurado=data_final
        ).order_by(
            "user",
        )

    return render(
        request,
        "banco_de_horas/calcula_banco_de_horas.html",
        {
            "banco_de_horas": banco_de_horas,
            "periodo_efetuado": data_final_object,
        },
    )


class BancoDeHorasListView(ListView):
    """View para listar o banco de horas."""

    def get_queryset(self) -> QuerySet[BancoDeHoras]:
        queryset = super().get_queryset().all().filter(user__userprofile__bateponto='Sim').order_by("user__username")
        user_name = self.request.GET.get('user_name')
        month_choice = self.request.GET.get('month_choice')

        if user_name:
            queryset = queryset.filter(user__username__icontains=user_name)

        if month_choice:
            selected_date = datetime.strptime(month_choice, '%d/%m/%Y')
            first_day = selected_date.replace(day=1).strftime('%Y-%m-%d')
            last_day = selected_date.replace(day=calendar.monthrange(selected_date.year, selected_date.month)[1]).strftime('%Y-%m-%d')

            queryset = queryset.filter(periodo_apurado__range=[first_day, last_day])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(userprofile__bateponto='Sim')
        context['form'] = SearchFilterForm(self.request.GET or None)
        context['user_name'] = self.request.GET.get('user_name', '')
        context['month_choice'] = self.request.GET.get('month_choice', '')
        return context


    model = BancoDeHoras
    template_name = "banco_de_horas/lista_banco_de_horas.html"
    context_object_name = "banco_de_horas"
    paginate_by = 10


class BancoDeHorasUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar o banco de horas."""

    model = BancoDeHoras
    form_class = BancoDeHorasForm
    context_object_name = "banco_de_horas"
    template_name = "banco_de_horas/atualizar_banco_de_horas.html"
    success_url = reverse_lazy("banco_de_horas:lista_banco_de_horas")


class BancoDeHorasDeleteView(LoginRequiredMixin, DeleteView):
    """View para deletar o banco de horas."""

    model = BancoDeHoras
    context_object_name = "banco_de_horas"
    template_name = "banco_de_horas/deletar_banco_de_horas.html"

    def get_success_url(self):
        """Retorna a URL de sucesso."""
        return reverse_lazy("banco_de_horas:lista_banco_de_horas")

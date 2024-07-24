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
from django.views.generic import DeleteView, UpdateView
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator

from .forms import BancoDeHorasForm, SearchFilterForm

import calendar

class BancoDeHorasListView(View):
    """View para listar o banco de horas."""

    model = BancoDeHoras
    template_name = "banco_de_horas/lista_banco_de_horas.html"
    context_object_name = "banco_de_horas"


    def get(self,request, *args, **kwargs):
        queryset = BancoDeHoras.objects.none()
        user_name = request.GET.get('user_name')
        month_choice = request.GET.get('month_choice')
        page_number = request.GET.get('page', 1)

        if user_name:
            queryset = BancoDeHoras.objects.all().filter(user__userprofile__bateponto='Sim', user_id=user_name)

        if month_choice:
            selected_date = datetime.strptime(month_choice, '%d/%m/%Y')
            first_day = selected_date.replace(day=1).strftime('%Y-%m-%d')
            last_day = selected_date.replace(day=calendar.monthrange(selected_date.year, selected_date.month)[1]).strftime('%Y-%m-%d')

            request.session['selected_data'] = last_day

            queryset = BancoDeHoras.objects.all().filter(periodo_apurado__range=[first_day, last_day], user__userprofile__bateponto='Sim').order_by("-periodo_apurado", "user__username")

        if user_name and month_choice:
            queryset = BancoDeHoras.objects.all().filter(periodo_apurado__range=[first_day, last_day], user__userprofile__bateponto='Sim', user_id=user_name).order_by("-periodo_apurado")


        paginator = Paginator(queryset, 30) # Paginação com 30 objetos por página
        page_obj = paginator.get_page(page_number)

        context = {
            'banco_de_horas': page_obj.object_list,
            'users': User.objects.filter(userprofile__bateponto='Sim'),
            'form': SearchFilterForm(request.GET or None),
            'user_name': user_name,
            'month_choice': month_choice,
            'page_obj': page_obj,
        }

        return render(request, 'banco_de_horas/lista_banco_de_horas.html', context)

    def post(self, request, *args, **kwargs):
        """Função para calcular o banco de horas"""

        # pega todos usuarios ativos
        users = User.objects.filter(
        is_active=True,
        userprofile__isnull=False,
        )
        # pega a data da competência selecionada no filtro
        data_final = request.session.get('selected_data')

        # cast data_final into datetime
        data_final_object = datetime.strptime(data_final, "%Y-%m-%d")

        # periodo anterios é o ultimo dia do mês anterior
        data_anterior = (data_final_object.replace(day=1) - timedelta(days=1)).strftime('%Y-%m-%d')
        data_inicial = data_final_object.replace(day=1).strftime('%Y-%m-%d')

        recalcular = request.POST.get('recalcular', 'false') == 'true'

        if BancoDeHoras.objects.check_banco_de_horas_existente(periodo=data_final_object):
            # confirm if the user wants to recalculate the banco de horas
            if not recalcular:
                return JsonResponse({
                    'status': 'warning',
                    'message': 'Banco de Horas já calculado. Deseja recalculá-lo?',
                    'check_banco_de_horas_existente': True
                })

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

        return JsonResponse({
            'status': 'success',
            'message': 'Banco de Horas calculado com sucesso!',
        })





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

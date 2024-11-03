"""
Views para o app refeicao
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

from datetime import datetime, date
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Refeicao
from user.models import UserProfile

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from refeicao.forms import RefeicaoForm



import pandas as pd
import calendar


def refeicao_listview(request, start_date: str = None, end_date: str = None):
    # Convert start_date and end_date to date objects if they are strings
    if start_date is not None:
        start_date = date.fromisoformat(start_date)
    else:
        start_date = date(2024, 11, 1)

    if end_date is not None:
        end_date = date.fromisoformat(end_date)
    else:
        end_date = date(2024, 11, 30)

    # Get all Users which is_active=True and related to UserProfile which have almoco = 'TODO DIA'
    users = User.objects.filter(is_active=True,).exclude(username='Admin').order_by("username")
    usuarios_que_almocam = sum(1 for user in users if user.userprofile.almoco == 'TODO DIA')
    usuarios_que_NAO_almocam = sum(1 for user in users if user.userprofile.almoco != 'TODO DIA')

    # Get the number of days between start_date and end_date without the weekends
    year, month = start_date.year, start_date.month
    _, num_days = calendar.monthrange(year, month)
    dates = [day for day in range(1, num_days + 1) if date(year, month, day).weekday() < 5]
    number_of_days = len(dates)

    # Create an empty DataFrame with dates as index and usernames as columns
    usernames = [user.username for user in users]
    pivot_df = pd.DataFrame(index=usernames, columns=dates)

    # Optionally, fill with sample data, e.g., 'Present'/'Absent' status
    # Here we leave it empty to be filled dynamically in the template
    for user in users:
        for day in dates:
            pivot_df.loc[user.username, day] = 'Sim' if user.userprofile.almoco == 'TODO DIA' or \
                Refeicao.objects.filter(usuario=user,
                                        data_refeicao__year=year,
                                        data_refeicao__month=month,
                                        data_refeicao__day=day).exists() else 'Não'

    # Convert the DataFrame to HTML for the template
    pivot_table_html = pivot_df.to_html(classes="table table-bordered table-striped", na_rep="", justify="justify-all",)

    # Get the name of the month in Brazilian Portuguese
    dict_meses = {'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'}
    nome_do_mes = calendar.month_name[month]
    nome_final = dict_meses[nome_do_mes]
    total_refeicoes = pivot_df.applymap(lambda x: 1 if x == 'Sim' else 0).sum().sum()

    return render(request, 'refeicao_report.html', {'pivot_table_html': pivot_table_html,
                                                    'nome_final': nome_final, 'ano': year,
                                                    'usuarios_que_almocam': usuarios_que_almocam,
                                                    'usuarios_que_NAO_almocam': usuarios_que_NAO_almocam,
                                                    'number_of_days': number_of_days, 'total_refeicoes': total_refeicoes})
class RefeicaoListView(LoginRequiredMixin, ListView):
    """ "Lista de refeições"""

    model = Refeicao
    template_name = "refeicao_list.html"
    context_object_name = "refeicoes"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Refeicao.objects.all().order_by("-data_refeicao")


class RefeicaoCreateView(LoginRequiredMixin, CreateView):
    """View para criar refeição"""

    model = Refeicao
    template_name = "refeicao_form.html"
    form_class = RefeicaoForm
    success_url = reverse_lazy("refeicao:refeicao_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        query = Refeicao.objects.get_queryset_usuario_data(
            self.request.user, form.instance.data_refeicao
        )
        if query.count() > 0:
            messages.error(
                self.request,
                "Refeição já cadastrada para esta data!",
            )
            return super().form_invalid(form)
        return super().form_valid(form)


class RefeicaoUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar refeição"""

    model = Refeicao
    template_name = "refeicao_form.html"
    form_class = RefeicaoForm
    success_url = reverse_lazy("refeicao:refeicao_list")


class RefeicaoDeleteView(LoginRequiredMixin, DeleteView):
    """View para deletar refeição"""

    model = Refeicao
    template_name = "refeicao_confirm_delete.html"
    success_url = reverse_lazy("refeicao:refeicao_list")


class RefeicaoDetailView(LoginRequiredMixin, DetailView):
    """View para detalhes de refeição"""

    model = Refeicao
    template_name = "refeicao_detail.html"
    context_object_name = "refeicao"


class SearchRefeicaoResultsView(ListView):
    """View para listar as férias filtradas."""

    paginate_by = 10
    model = Refeicao
    template_name = "refeicao_list.html"
    context_object_name = "refeicoes"

    def get_queryset(self):  # new
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            refeicoes = Refeicao.objects.filter(Q(usuario__username__icontains=query))
        else:  # pragma: no cover
            refeicoes = Refeicao.objects.all()

        return refeicoes

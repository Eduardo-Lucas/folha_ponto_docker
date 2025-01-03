"""
Views para o app refeicao
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

from datetime import datetime, date, timedelta
from django.contrib.auth.models import User, Group
from django.shortcuts import render

from apontamento.models import Ponto
from feriado.models import Feriado

from .models import Refeicao

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from refeicao.forms import RefeicaoForm, RefeicaoListForm

from django.views.generic import TemplateView
from django.utils import timezone
import pandas as pd
import calendar
from collections import defaultdict
from calendar import monthrange
import holidays
from django.db.models import Prefetch

country_holidays = holidays.BR()




def get_business_days(year, month):
    """Utility function to get the number of business days in a month"""
    num_days = monthrange(year, month)[1]
    days = [
        day for day in range(1, num_days + 1)
            if date(year, month, day).weekday() < 5 and date(year, month, day) not in country_holidays
    ]
    return days

class MonthlyReportView(TemplateView):
    template_name = 'monthly_report.html'

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    # Retrieve month and year from parameters (use current month/year if not provided)
    year = self.request.GET.get('year', timezone.now().year)
    month = self.request.GET.get('month', timezone.now().month)
    year, month = int(year), int(month)

    # Get business days for the month
    business_days = get_business_days(year, month)

    # Fetch groups and users dynamically
    groups = Group.objects.prefetch_related(
        Prefetch('user_set', queryset=User.objects.filter(is_active=True).exclude(username='Admin').order_by('username'))
    )

    # Simulating or retrieving actual report data
    report_data = {
        user.username: {day: self.get_user_data_for_day(user, day, year, month) for day in business_days}
        for group in groups for user in group.user_set.all()
    }

    # Prepare the data structure to be passed to the template
    data_by_group = {}
    grand_total = defaultdict(int)  # Stores grand totals per day
    group_totals = defaultdict(int)  # Stores total 'Sim' counts per group

    for group in groups:
        group_total = defaultdict(int)  # Stores subtotal per day for each group
        user_data = []

        for user in group.user_set.all():
            user_row = {
                'name': user.username,
                'days': [1 if report_data.get(user.username, {}).get(day) == 'Sim' else 0 for day in business_days]
            }

            # Calculate daily totals for each user and update group totals
            for day, value in zip(business_days, user_row['days']):
                group_total[day] += value
                grand_total[day] += value

            # Count 'Sim' values for the user
            user_sim_count = sum(user_row['days'])
            group_totals[group.name] += user_sim_count

            user_data.append(user_row)

        data_by_group[group.name] = {
            'users': user_data,
            'subtotal': [group_total[day] for day in business_days]
        }

    # Grand total for all groups across all business days
    context['data_by_group'] = data_by_group
    context['grand_total'] = [grand_total[day] for day in business_days]
    context['business_days'] = business_days
    context['business_days_length_plus_one'] = len(business_days) + 1
    context['group_totals'] = group_totals
    context['grand_total_sim'] = sum(group_totals.values())

    return context

def get_user_data_for_day(self, user, day, year, month):
    """
    Placeholder method to retrieve or simulate user's data for a given day.
    Replace this with the actual logic to fetch daily user data.
    """
    # Example: simulate data, or replace with actual query to retrieve user's data for 'day'
    return 'Sim' if user.userprofile.almoco == 'TODO DIA' or \
                Refeicao.objects.filter(usuario=user,
                                        data_refeicao__year=year,
                                        data_refeicao__month=month,
                                        data_refeicao__day=day).exists() else 'Não'

def refeicao_listview(request, start_date: str = None, end_date: str = None):
    if request.method == 'POST':
        form = RefeicaoListForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['data_inicial']
            end_date = form.cleaned_data['data_final']
            if start_date > end_date:
                messages.error(request, 'Data inicial não pode ser maior que a data final.')
                return render(request, 'refeicao_report.html', {'form': form})

    else:
        form = RefeicaoListForm()
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date is not None:
            start_date = date.fromisoformat(start_date)
        else:
            start_date = datetime.now().replace(day=1).date()

        if end_date is not None:
            end_date = date.fromisoformat(end_date)
        else:
            end_date = datetime.now().date()

    # Get all Users which is_active=True and related to UserProfile which have almoco = 'TODO DIA'
    users = User.objects.filter(is_active=True, userprofile__almoco__in=['TODO DIA', 'EVENTUAL']).exclude(username='Admin').order_by("username")
    usuarios_que_almocam = len(users)  # sum(1 for user in users if user.userprofile.almoco == 'TODO DIA')
    # usuarios_que_NAO_almocam = sum(1 for user in users if user.userprofile.almoco != 'TODO DIA')

    # Get the number of days between start_date and end_date without the weekends
    year, month = start_date.year, start_date.month
    num_days = (end_date - start_date).days + 1

    # Query the Feriado model to get the list of holidays within the date range
    feriados_fixos = list(Feriado.objects.filter(
        month__range=[start_date.month, end_date.month],
        dia__range=[start_date.day, end_date.day]
    ).values_list('month', 'dia'))

    # add the year to the fixed holidays
    feriados_fixos = [(year, mes, dia) for dia, mes in feriados_fixos]
    feriados_fixos = [date(*t) for t in feriados_fixos]
    print("FERIADOS FIXOS=> ", feriados_fixos)


    feriados_nao_fixos = list(Feriado.objects.filter(
        dia__range=[start_date.day, end_date.day],
        month__range=[start_date.month, end_date.month],
        ano__range=[start_date.year, end_date.year]
    ).values_list('ano', 'month', 'dia'))

    feriados_nao_fixos = [(ano, mes, dia) for dia, mes, ano in feriados_nao_fixos]
    feriados_nao_fixos = [date(*t) for t in feriados_nao_fixos]

    feriados = feriados_fixos + feriados_nao_fixos

    # Create a list of dates excluding weekends and holidays
    dates = [day for day in range(1, num_days + 1) if date(year, month, day).weekday() < 6 and date(year, month, day) not in feriados]
    number_of_days = len(dates)

    # raise a warning message if there are no business days in the date range
    if number_of_days == 0:
        messages.warning(request, 'Não há dias úteis no intervalo de datas fornecido.')
        return render(request, 'refeicao_report.html', {'form': form})


    # Create an empty list to store user activity data
    data = []

    # Populate data for each user and each day in the date range
    for user in users:
        groups = user.groups.all()  # Get all groups for the user
        group_names = ', '.join(group.name for group in groups)  # Join group names into a single string
        for day in dates:
            value = 'X' if (user.userprofile.almoco == 'TODO DIA' and


                            not Refeicao.objects.filter(usuario=user,
                                                        data_refeicao__year=year,
                                                        data_refeicao__month=month,
                                                        data_refeicao__day=day,
                                                        consumo=False).exists()) or \
                           Refeicao.objects.filter(usuario=user,
                                                   data_refeicao__year=year,
                                                   data_refeicao__month=month,
                                                   data_refeicao__day=day,
                                                   consumo=True).exists() else \
                    '' if Refeicao.objects.filter(usuario=user,
                                                  data_refeicao__year=year,
                                                  data_refeicao__month=month,
                                                  data_refeicao__day=day,
                                                  consumo=False).exists() else ''
            data.append({
                'Grupo': group_names,
                'Usuário': user.username,
                'Dia do Mês': day,
                'value': value
            })

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Ensure the DataFrame contains the 'value' column
    if 'value' not in df.columns:
        raise KeyError("The DataFrame does not contain the 'value' column")

    # Create pivot table: Users and Groups on Y-axis, Days of the month on X-axis
    pivot_table = df.pivot_table(
        values='value',
        index=['Grupo', 'Usuário'],
        columns='Dia do Mês',
        aggfunc=lambda x: 'X' if 'X' in x.values else '',
        fill_value=''
    )

    # Calculate subtotal for each group
    group_totals = pivot_table.apply(lambda x: x.map(lambda y: int(1) if y == 'X' else int(0))).groupby(level='Grupo').sum()
    group_totals['Total'] = group_totals.sum(axis=1)

    # Convert group_totals to integers
    group_totals = group_totals.astype(int)

    # Calculate grand total
    grand_total = group_totals.sum(axis=0)
    grand_total.name = 'Total Geral'

    # Convert grand_total to integers
    grand_total = grand_total.astype(int)

    # Append the totals to the pivot table using pd.concat
    pivot_table = pd.concat([pivot_table, group_totals])
    pivot_table = pd.concat([pivot_table, pd.DataFrame(grand_total).T])

    # Convert pivot table to HTML for display
    pivot_table_html = pivot_table.to_html(classes="table table-bordered table-striped table-hover table-sm", na_rep="",
                                           justify="center", decimal=',', float_format='%.0f', col_space=25, border=0)

    # Get the name of the month in Brazilian Portuguese
    dict_meses = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril',
        'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto',
        'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'}

    nome_do_mes = calendar.month_name[month]
    nome_final = dict_meses[nome_do_mes]

    total_refeicoes = df.apply(lambda x: x.map(lambda y: int(1) if y == 'X' else int(0))).sum().sum()
    total_refeicoes = int(total_refeicoes)

    return render(request, 'refeicao_report.html', {'pivot_table_html': pivot_table_html,
                                                    'nome_final': nome_final, 'ano': year,
                                                    'usuarios_que_almocam': usuarios_que_almocam,
                                                    'number_of_days': number_of_days,
                                                    'total_refeicoes': total_refeicoes,
                                                    'form': form})
def user_activity_report(request):
    # Get all active users and their related groups
    users = User.objects.filter(is_active=True).exclude(username='Admin').order_by("username")

    # Define the month of November
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2024, 11, 30)
    days_in_november = (end_date - start_date).days + 1  # Get number of days in November where they are not weekends
    days_in_november = sum(1 for day in range(days_in_november) if (start_date + timedelta(days=day)).weekday() < 5)

    # Create an empty list to store user activity data
    data = []

    # Populate data for each user and each day in November
    for user in users:
        groups = user.groups.all()  # Get all groups for the user
        group_names = ', '.join(group.name for group in groups)  # Join group names into a single string
        for day_offset in range(days_in_november):
            date = start_date + timedelta(days=day_offset)
            data.append({
                'Grupo': group_names,
                'Usuário': user.username,
                'Data': date.day,
                'value': 'Sim' if user.userprofile.almoco == 'TODO DIA' or Refeicao.objects.filter(usuario=user, data_refeicao=date).exists() else 'Não'
            })

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Create pivot table: Users and Groups on Y-axis, Days of November on X-axis
    pivot_table = df.pivot_table(
        values='value',
        index=['Grupo', 'Usuário'],
        columns='Data',
        aggfunc='sum',
        fill_value=0
    )

    # Convert pivot table to HTML for display
    pivot_html = pivot_table.to_html(classes="table table-striped")

    # Render the template with the report
    return render(request, 'user_activity_report.html', {'pivot_html': pivot_html})

class RefeicaoListView(LoginRequiredMixin, ListView):
    """ "Lista de refeições"""

    model = Refeicao
    template_name = "refeicao_cadastrada.html"
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


        # cannot create a refeicao if it is a Sunday
        if form.instance.data_refeicao.weekday() == 6:
            messages.error(
                self.request,
                "Não é possível cadastrar refeição no Domingo!",
            )
            return super().form_invalid(form)

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

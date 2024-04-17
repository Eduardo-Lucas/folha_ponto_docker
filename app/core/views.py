from datetime import datetime

from ferias.models import Ferias
from apontamento.models import Ponto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render


@login_required
def home(request):
    """Home Page"""
    users = User.objects.filter(is_active=True)

    pontos_abertos = []
    pontos_fechados = []

    for user in users:
        ponto = Ponto.objects.filter(usuario=user).last()

        if ponto:
            cliente = ponto.cliente_id if ponto.cliente_id else None
            tarefa = ponto.tipo_receita if ponto.tipo_receita else "Contábil"
            total_dia = Ponto.objects.total_day_time(
                day=ponto.entrada.date(), user=user
            )
            if ponto.saida:
                last_interaction = ponto.saida
            else:
                last_interaction = ponto.entrada

            ponto_status = Ponto.objects.get_open_pontos(user)

            ferias = Ferias.objects.get_ferias(
                last_interaction.date(), last_interaction.date(), user
            )

            if ponto_status.count() > 0:

                pontos_abertos.append(
                    {
                        "usuario": user,
                        "ferias": ferias,
                        "last_interaction": last_interaction,
                        "day": last_interaction.date(),
                        "cliente": cliente,
                        "tarefa": tarefa,
                        "total_dia": total_dia,
                        "tarefa_aberta": ponto_status,
                    }
                )
            else:

                pontos_fechados.append(
                    {
                        "usuario": user,
                        "ferias": ferias,
                        "last_interaction": last_interaction,
                        "day": last_interaction.date(),
                        "cliente": cliente,
                        "tarefa": tarefa,
                        "total_dia": total_dia,
                        "tarefa_aberta": ponto_status,
                    }
                )

            # sort pontos by last_interaction desc and tarefa_aberta
            pontos_abertos = sorted(
                pontos_abertos, key=lambda k: k["last_interaction"], reverse=True
            )
            pontos_fechados = sorted(
                pontos_fechados, key=lambda k: k["last_interaction"], reverse=True
            )

    paginator_pontos_abertos = Paginator(pontos_abertos, 10)
    paginator_pontos_fechados = Paginator(pontos_fechados, 10)

    page = request.GET.get("page")

    pontos_abertos = paginator_pontos_abertos.get_page(page)
    pontos_fechados = paginator_pontos_fechados.get_page(page)

    # proximas ferias a serem tiradas
    proximas_ferias = Ferias.objects.get_proximas_ferias()

    paginator_proximas_ferias = Paginator(proximas_ferias, 10)
    proximas_ferias = paginator_proximas_ferias.get_page(page)

    context = {
        "pontos_abertos": pontos_abertos,
        "pontos_fechados": pontos_fechados,
        "proximas_ferias": proximas_ferias,
    }

    # Carrega as datas iniciais e finais na sessão
    carrega_datas_session(request)

    return render(request, "core/home.html", context)


def carrega_datas_session(request, user_id=None):
    """Carrega as datas iniciais e finais na sessão"""
    now = datetime.now()

    # Set data inicial
    first_day = now.replace(day=1).strftime("%Y-%m-%d")
    # turn first_day into a datetime object
    # first_day = datetime.strptime(first_day, "%Y-%m-%d")
    request.session["data_inicial"] = first_day

    # Set data final
    last_day = now.strftime("%Y-%m-%d")
    # turn last_day into a datetime object
    # last_day = datetime.strptime(last_day, "%Y-%m-%d")
    request.session["data_final"] = last_day

    if user_id is None:
        # Set user_id
        try:
            user = User.objects.get(username=request.user)
            request.session["user_id"] = user.id
        except ObjectDoesNotExist:  # Replace DoesNotExist with ObjectDoesNotExist
            request.session["user_id"] = None

    else:
        request.session["user_id"] = user_id

from apontamento.models import Ponto
from django.contrib.auth.models import User
from django.db.models import F, Max, Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Home Page"""
    users = User.objects.all().order_by("username")
    pontos = []
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

            pontos.append(
                {
                    "usuario": user,
                    "last_interaction": last_interaction,
                    "day": last_interaction.date(),
                    "cliente": cliente,
                    "tarefa": tarefa,
                    "total_dia": total_dia,
                }
            )

            # sort pontos by last_interaction desc
            pontos = sorted(pontos, key=lambda k: k["last_interaction"], reverse=True)

    return render(request, "core/home.html", {"pontos": pontos})

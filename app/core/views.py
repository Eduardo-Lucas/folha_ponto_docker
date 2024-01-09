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
            pontos.append(
                {
                    "usuario": user,
                    "last_interaction": ponto.entrada,
                    "cliente": cliente,
                    "tarefa": tarefa,
                    "total_dia": total_dia,
                }
            )

    return render(request, "core/home.html", {"pontos": pontos})

from datetime import datetime, timedelta

from apontamento.models import Ponto
from django.db.models import Q


class PontoService:
    """Classe de serviços para o apontamento"""

    def ponto_list(self, usuario_id, data_inicial, data_final):
        """Retorna os pontos do usuário no período"""
        query = Ponto.objects.filter(
            usuario=usuario_id,
            entrada__range=(data_inicial, data_final),
        ).order_by("entrada")

        return query

    def muda_tarefa(self, usuario_id):
        """Muda a tarefa do último ponto do usuário"""
        check = Ponto.objects.filter(
            entrada__date=datetime.now().date(), usuario=usuario_id
        ).last()
        if check.saida is None:
            check.saida = datetime.now()
            check.save()
            return True
        return False

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


from django.db.models import Q
from apontamento.models import Ponto
from datetime import timedelta


class PontoService:
    def ponto_list(self, usuario_id, data_inicial, data_final):
        query = Ponto.objects.filter(
            usuario=usuario_id,
            entrada__range=(data_inicial, data_final),
        ).order_by('entrada')

        return query

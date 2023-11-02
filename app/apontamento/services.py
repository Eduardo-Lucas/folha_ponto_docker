from django.db.models import Q
from apontamento.models import Ponto


class PontoService:
    def ponto_list(self, usuario_id, data_inicial, data_final):
        data_query = Q(
            Q(
                entrada__gte=data_inicial,
            )
            & Q(
                saida__lte=data_final,
            )
        )
        query = Ponto.objects.filter(data_query, usuario_id=usuario_id)

        return query

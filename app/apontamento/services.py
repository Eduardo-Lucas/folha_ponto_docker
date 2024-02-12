from datetime import timedelta
from django.db.models import Sum, Case, When, F, DurationField
from django.db.models.functions import ExtractDay
from apontamento.models import Ponto



class PontoService:
    """Classe de serviços para o apontamento"""

    def ponto_list(self, usuario_id, data_inicial, data_final):
        """Retorna os pontos do usuário no período"""
        query = Ponto.objects.filter(
            usuario=usuario_id,
            entrada__range=(data_inicial, data_final),
        ).order_by("entrada")

        return query

    def totaliza_ponto(self, usuario_id, data_inicial, data_final):
        """Retorna o total de horas trabalhadas em um intervalo de datas"""
        query = (
            Ponto.objects.filter(
                usuario=usuario_id,
                entrada__range=(data_inicial, data_final + timedelta(days=2)),
            )
            .annotate(
                date=ExtractDay("entrada"),
                horas_trabalhadas=Sum(
                    F("saida") - F("entrada"), output_field=DurationField()
                ),
            )
            .annotate(
                total_credito=Case(
                    When(
                        horas_trabalhadas__gt=timedelta(hours=8),
                        then=F("horas_trabalhadas") - timedelta(hours=8),
                    ),
                    default=timedelta(hours=0),
                    output_field=DurationField(),
                ),
                total_debito=Case(
                    When(
                        horas_trabalhadas__lt=timedelta(hours=8),
                        then=timedelta(hours=8) - F("horas_trabalhadas"),
                    ),
                    default=timedelta(hours=0),
                    output_field=DurationField(),
                ),
            )
            .values("date", "horas_trabalhadas", "total_credito", "total_debito")
        )

        return query

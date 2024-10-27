import django_filters
from django_filters import DateFilter
from .models import Ponto

class PontoFilter(django_filters.FilterSet):

    entrada__gte = DateFilter(
        field_name="entrada",
        lookup_expr="gte",
        label="Início",
        input_formats=["%Y-%m-%d", "%d/%m/%Y"]
    )
    saida__lte = DateFilter(
        field_name="saida",
        lookup_expr="lte",
        label="Fim",
        input_formats=["%Y-%m-%d", "%d/%m/%Y"]
    )
    class Meta:
        model = Ponto

        fields = ['entrada__gte', 'saida__lte', 'usuario', 'cliente_id', 'tipo_receita']


    def __init__(self, *args, **kwargs):
        super(PontoFilter, self).__init__(*args, **kwargs)

        self.filters["entrada__gte"].required = True
        self.filters["saida__lte"].required = True

        self.filters["usuario"].label = "Usuário"
        self.filters["usuario"].required = False
        self.filters["cliente_id"].label = "Cliente"
        self.filters["cliente_id"].required = False
        self.filters["tipo_receita"].label = "Tarefa"
        self.filters["tipo_receita"].required = False

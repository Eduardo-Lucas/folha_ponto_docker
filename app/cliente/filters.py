import django_filters

from .models import Cliente

class ClienteFilter(django_filters.FilterSet):

    custom_codigosistema = django_filters.CharFilter(field_name="codigosistema", method="filter_codigosistema", label="Código")
    nomerazao = django_filters.CharFilter(field_name="nomerazao", lookup_expr="icontains", label="Razão Social")
    documento = django_filters.CharFilter(field_name="documento", lookup_expr="icontains", label="CPF/CNPJ")


    def filter_codigosistema(self, queryset, name, value):
        # Strip leading zeros from user input
        # value = value.lstrip("0")
        # Filter queryset based on modified value
        return queryset.filter(**{name: value})

    class Meta:
        model = Cliente

        fields = ['custom_codigosistema', 'nomerazao', 'documento']


    def __init__(self, *args, **kwargs):
        super(ClienteFilter, self).__init__(*args, **kwargs)
        self.filters["custom_codigosistema"] = django_filters.CharFilter(field_name="codigosistema", method=self.filter_codigosistema, label="Código")
        self.filters["nomerazao"].label = "Razão Social"
        self.filters["documento"].label = "CPF/CNPJ"

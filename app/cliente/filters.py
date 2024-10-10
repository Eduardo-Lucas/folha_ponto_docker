import django_filters

from .models import Cliente

class ClienteFilter(django_filters.FilterSet):
    def filter_codigosistema(self, queryset, name, value):
        # Strip leading zeros from user input
        value = value.lstrip("0")
        # Filter queryset based on modified value
        return queryset.filter(**{name: value})

    class Meta:
        model = Cliente

        fields = {
            "nomerazao": ["icontains"],
            # "codigosistema": ["icontains"],
            "documento": ["icontains"],

        }

    def __init__(self, *args, **kwargs):
        super(ClienteFilter, self).__init__(*args, **kwargs)
        self.filters["nomerazao__icontains"].label = "Razão Social"
        self.filters["documento__icontains"].label = "CPF/CNPJ"
        self.filters["custom_codigosistema"] = django_filters.CharFilter(field_name="codigosistema", method=self.filter_codigosistema, label="Código")

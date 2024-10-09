import django_filters

from .models import Cliente

class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = Cliente

        fields = {
            "nomerazao": ["icontains"],
            "codigosistema": ["icontains"],

        }

    def __init__(self, *args, **kwargs):
        super(ClienteFilter, self).__init__(*args, **kwargs)
        self.filters["nomerazao__icontains"].label = "Razão Social"
        self.filters["codigosistema__icontains"].label = "Código"

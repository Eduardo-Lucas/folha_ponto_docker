import django_filters

from .models import Cliente

class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = Cliente

        fields = {
            "nomerazao": ["icontains"],
            "codigosistema": ["icontains"],

        }

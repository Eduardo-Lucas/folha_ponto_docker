import django_filters

from .models import Ferias

class FeriasFilter(django_filters.FilterSet):

    class Meta:
        model = Ferias

        fields = ['user', 'data_inicio', ]

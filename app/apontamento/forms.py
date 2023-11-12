from django import forms
from django.contrib.auth.models import User
from apontamento.models import Ponto
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = "date"


class FolhaPontoForm(forms.Form):
    entrada = forms.DateField(widget=DateInput, label="Início", required=True)
    saida = forms.DateField(widget=DateInput, label="Fim", required=True)
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        entrada = cleaned_data.get('entrada')
        saida = cleaned_data.get('saida')

        if entrada and saida:
            if entrada > saida:
                raise ValidationError("Data inicial cannot be greater than data final")

        return cleaned_data
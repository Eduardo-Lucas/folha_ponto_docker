from django import forms
from django.contrib.auth.models import User
from apontamento.models import Ponto


class DateInput(forms.DateInput):
    input_type = "date"


class FolhaPontoForm(forms.Form):
    entrada = forms.DateField(widget=DateInput, label="Início", required=False)
    saida = forms.DateField(widget=DateInput, label="Fim", required=False)
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

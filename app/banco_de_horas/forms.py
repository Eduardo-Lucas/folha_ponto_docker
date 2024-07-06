""" Formulário para o modelo BancoDeHoras """

from datetime import timedelta
from django import forms

from apontamento.templatetags.timedelta_filters import format_timedelta

from .models import BancoDeHoras



class BancoDeHorasForm(forms.ModelForm):
    """Formulário para criar um novo banco de horas."""

    class Meta:
        """Meta definição para o formulário de BancoDeHoras."""

        model = BancoDeHoras

        fields = (
            "user",
            "periodo_apurado",
            "saldo_anterior",
            "total_credor",
            "total_devedor",
            "compensacao",
            "pagamento",
        )

    # disabel user field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].disabled = True
        self.fields["periodo_apurado"].disabled = True


class UserFilterForm(forms.Form):
        """Campo para filtrar a lista do banco de horas por nome"""
        user_name = forms.CharField(
             label="Filtrar por nome de usuário",
             max_length=100,
             required=False,
             widget=forms.TextInput(
                  attrs={
                       'class':'form-control',
                       'placeholder':'Digite o nome do usuário'
                  }
             )
        )

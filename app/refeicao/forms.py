"""Formulários para refeição"""

from datetime import datetime

from apontamento.forms import DateInput
from django import forms

from .models import Refeicao


class RefeicaoForm(forms.ModelForm):
    """Formulário para refeição"""

    class Meta:
        """Meta informações do formulário"""

        model = Refeicao
        fields = [
            "usuario",
            "data_refeicao",
            "consumo",
            "observacao",
        ]
        widgets = {
            "data_refeicao": DateInput(format="%Y-%m-%d"),
            "observacao": forms.Textarea(attrs={"rows": 3}),
        }

    # data_refeicao initial value is current day
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # get activer Users from User to populate a select field
        self.fields["usuario"].queryset = self.fields["usuario"].queryset.filter(
            is_active=True
        ).exclude(username='Admin').order_by("username")

        self.fields["data_refeicao"].initial = datetime.now().date()
        self.fields["observacao"].required = False
        self.fields["consumo"].initial = True


class RefeicaoListForm(forms.Form):
    """Formulário para escolher, via select, o período inicial e final para listar as refeições"""

    data_inicial = forms.DateField(widget=DateInput(format="%Y-%m-%d"))
    data_final = forms.DateField(widget=DateInput(format="%Y-%m-%d"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["data_inicial"].initial = datetime.now().replace(day=1).date()
        self.fields["data_final"].initial = datetime.now().date()

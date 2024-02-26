"""
User Forms
"""
from django import forms
from apontamento.models import TipoReceita
from .models import UserProfile


class LoginForm(forms.Form):
    """Login Form"""

    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class UserProfileform(forms.ModelForm):
    """User Profile Form"""
    # Bruno pediu para comentar esses campos
    # situacaoentidade = forms.CharField(label="Situação Entidade")
    # contato_id = forms.CharField(label="Contato")
    bateponto = forms.CharField(
        label="Bate Ponto",
        required=False,
        widget=forms.Select(choices=UserProfile.bate_ponto_choices),
    )
    semintervaloalmoco = forms.CharField(
        label="Sem Intervalo Almoço",
        required=False,
        widget=forms.Select(choices=UserProfile.sem_intervalo_almoco_choices),
    )
    cargahoraria = forms.IntegerField(
        label="Carga Horária", help_text="Entre 4 e 8 horas. Só Admin altera."
    )
    almoco = forms.CharField(
        label="Almoço",
        required=False,
        widget=forms.Select(choices=UserProfile.almoco_choices),
    )

    class Meta:
        """User Profile Meta Class"""

        model = UserProfile
        fields = (
            "user",
            # "situacaoentidade",
            # "contato_id",
            "bateponto",
            "cargahoraria",
            "departamento",
            "semintervaloalmoco",
            "nome",
            "email",
            "tipo_receita",
            "almoco",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cargahoraria"].widget.attrs["readonly"] = True
        self.fields["tipo_receita"].queryset = TipoReceita.objects.get_active()

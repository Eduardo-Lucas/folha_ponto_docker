from django import forms

from .models import UserProfile


class LoginForm(forms.Form):
    """Login Form"""

    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class UserProfileform(forms.ModelForm):
    """User Profile Form"""

    situacaoentidade = forms.CharField(label="Situação Entidade")
    contato_id = forms.CharField(label="Contato")
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
    cargahoraria = forms.IntegerField(label="Carga Horária")
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
            "situacaoentidade",
            "contato_id",
            "bateponto",
            "cargahoraria",
            "departamento",
            "semintervaloalmoco",
            "nome",
            "email",
            "tipo_receita",
            "almoco",
        )

from apontamento.models import Ponto, TipoReceita
from django import forms
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    """DateInput."""

    input_type = "date"


class DateTimeInput(forms.DateTimeInput):
    """DateTimeInput."""

    input_type = "datetime-local"


class TimeInput(forms.TimeInput):
    """TimeInput."""

    input_type = "time"


class FolhaPontoForm(forms.Form):
    """Form for creating a new appointment."""

    entrada = forms.DateField(widget=DateInput, label="Início", required=True)
    saida = forms.DateField(widget=DateInput, label="Fim", required=True)
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("username"), required=True
    )


class AppointmentForm(forms.ModelForm):
    """Form for creating a new appointment."""

    class Meta:
        """Meta definition for Appointmentform."""

        model = Ponto
        fields = (
            "entrada",
            "primeiro",
            "segundo",
            "atraso",
            "saida",
            "usuario",
            "fechado",
            "cliente_id",
            "tipo_receita",
            "atrasoautorizado",
        )
        widgets = {
            "entrada": DateTimeInput(),
            "saida": DateTimeInput(),
        }

    def __init__(self, *args, day=None, user_id=None, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.day = day
        self.user_id = (
            user_id
            if user_id is not None
            else User.objects.filter(username=["usuario"]).first().id
        )
        # You can now use self.day and self.user_id in your form


class AppointmentUpdateForm(forms.ModelForm):
    """Form for updating an existing appointment."""

    class Meta:
        """Meta definition for AppointmentUpdateform."""

        model = Ponto
        fields = ("entrada", "saida", "usuario")
        widgets = {
            "entrada": DateTimeInput(),
            "saida": DateTimeInput(),
        }


class AppointmentCreateForm(forms.ModelForm):
    """Form for creating a new appointment."""

    class Meta:
        """Meta definition for Appointmentform."""

        model = Ponto
        fields = (
            "tipo_receita",
            "cliente_id",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tipo_receita"].required = True
        self.fields["tipo_receita"].initial = 1
        self.fields["tipo_receita"].queryset = TipoReceita.objects.get_active()

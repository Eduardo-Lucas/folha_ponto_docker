""" Forms for the apontamento app. """

from calendar import monthrange
from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Ponto, TipoReceita


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

    def get_last_day_month(self, year, month):
        """Return the last day of a month."""
        _, last_day = monthrange(year, month)
        return last_day

    entrada = forms.DateField(widget=DateInput, label="Início", required=True)
    saida = forms.DateField(widget=DateInput, label="Fim", required=True)
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("username"),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        # Get the user from the kwargs
        self.user = kwargs.pop("user", None)
        super(FolhaPontoForm, self).__init__(*args, **kwargs)
        # Get the current date
        now = datetime.now()
        # Get the first day of the current month
        first_day = now.replace(day=1).strftime("%Y-%m-%d")
        # Set the initial value of the entrada field
        self.fields["entrada"].initial = first_day

        # Get the last day of the current month
        last_day = self.get_last_day_month(now.year, now.month)
        # Set the initial value of the saida field
        self.fields["saida"].initial = now.replace(day=last_day).strftime("%Y-%m-%d")

        # Set the initial value of the usuario field
        if self.user is not None:
            self.fields["usuario"].initial = self.user


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

    def __init__(self, *args, day=None, user_id=None, tipo_receita=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.day = day
        self.user_id = (
            user_id
            if user_id is not None
            else User.objects.filter(username=["usuario"]).first().id
        )
        self.fields["tipo_receita"].required = True

    def clean_tipo_receita(self):
        """Validates the tipo_receita field."""
        tipo_receita = self.cleaned_data.get("tipo_receita")
        if tipo_receita and tipo_receita.status == "Inativo":
            raise ValidationError("TipoReceita cannot be Inativo.")
        return tipo_receita


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

    cliente = forms.CharField(max_length=200)

    class Meta:
        """Meta definition for Appointmentform."""

        model = Ponto
        fields = (
            "tipo_receita",
            "cliente",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tipo_receita
        self.fields["tipo_receita"].required = True
        self.fields["tipo_receita"].initial = 1
        self.fields["tipo_receita"].queryset = TipoReceita.objects.get_active()
        # cliente
        self.fields["cliente"].required = True

    # field cliente cannot be null
    def clean_cliente(self):
        """Validates the cliente field."""
        cliente = self.cleaned_data.get("cliente")
        if not cliente:
            raise ValidationError("Cliente cannot be null.")
        return cliente

""" Forms for the apontamento app. """

from calendar import monthrange
from datetime import datetime, timedelta

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
        queryset=User.objects.filter(is_active=True).order_by("username"),
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
        # last_day = self.get_last_day_month(now.year, now.month)
        # Set the initial value of the saida field
        self.fields["saida"].initial = now.strftime("%Y-%m-%d")

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


class AjustePontoForm(forms.ModelForm):
    """Form for creating a new appointment."""

    class Meta:
        """Meta definition for Appointmentform."""

        model = Ponto
        fields = (
            "entrada",
            "saida",
            "tipo_receita",
            "cliente_id",
            "fechado",
        )
        widgets = {
            "entrada": DateTimeInput(),
            "saida": DateTimeInput(),
        }

    def __init__(
        self, *args, day=None, user_id=None, tipo_receita=None, request=None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.day = day
        # self.user_id = (
        #     user_id
        #     if user_id is not None
        #     else User.objects.filter(username=["usuario"]).first().id
        # )
        self.fields["tipo_receita"].required = True
        self.fields["saida"].required = True

    def clean_tipo_receita(self):
        """Validates the tipo_receita field."""
        tipo_receita = self.cleaned_data.get("tipo_receita")
        if tipo_receita and tipo_receita.status == "Inativo":
            raise ValidationError("Tipo de Receita não pode estar Inativo.")
        return tipo_receita

    # validate if entrada is greater than saida
    def clean(self):
        """Validates the entrada and saida fields."""
        cleaned_data = super().clean()
        entrada = cleaned_data.get("entrada")
        saida = cleaned_data.get("saida")
        if entrada and saida:
            if entrada > saida:
                raise ValidationError("Entrada não pode ser maior que Saída.")

            # entrada cannot be in the future
            if entrada > datetime.now():
                raise ValidationError("Entrada não pode ser no futuro.")

            # saida cannot be in the future
            if saida > datetime.now():
                raise ValidationError("Saída não pode ser no futuro.")

            if saida - entrada > timedelta(hours=10):
                raise ValidationError("Jornada não pode ser maior que 10 horas.")
        return cleaned_data

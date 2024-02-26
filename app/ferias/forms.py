from django import forms
from ferias.models import Ferias


class DateInput(forms.DateInput):
    """DateInput."""

    input_type = "date"


class FeriasForm(forms.ModelForm):
    """Form definition for Ferias."""

    cumpriu = forms.BooleanField(
        label="Cumpriu",
        required=False,
        help_text="Se marcado, indica que o período já foi cumprido.",
    )

    class Meta:
        """Meta definition for FeriasForm."""

        model = Ferias
        fields = ("user", "periodo", "data_inicial", "data_final", "cumpriu")
        widgets = {
            "data_inicial": forms.DateInput(),
            "data_final": forms.DateInput(),
        }

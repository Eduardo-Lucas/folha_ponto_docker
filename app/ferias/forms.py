"""
Module docstring describing the purpose of the module.
"""

from datetime import datetime

from django import forms
from django.contrib.auth.models import User
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
        fields = (
            "user",
            "periodo",
            "data_inicial",
            "data_final",
            "dias_uteis",
            "cumpriu",
        )

        widgets = {
            "data_inicial": DateInput(format="%Y-%m-%d"),
            "data_final": DateInput(format="%Y-%m-%d"),
        }

    def get_object(self):
        """get_object."""
        return self.instance

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(FeriasForm, self).__init__(*args, **kwargs)
        self.fields["user"].initial = User.objects.get(
            id=self.request.session.get("user_id")
        )
        self.fields["periodo"].initial = datetime.now().year
        self.fields["dias_uteis"].initial = 1
        self.fields["dias_uteis"].widget.attrs["readonly"] = True

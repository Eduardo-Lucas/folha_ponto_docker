""" Formulário para o modelo BancoDeHoras """

from datetime import timedelta, datetime
import calendar
from django import forms
from django.contrib.auth.models import User

from apontamento.templatetags.timedelta_filters import format_timedelta
from .utils import get_previous_month_choices
import re


from .models import BancoDeHoras, ValorInserido



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
        self.fields["compensacao"].disabled = True
        self.fields["pagamento"].disabled = True

class SearchFilterForm(forms.Form):
        """Campo para filtrar a lista do banco de horas por nome"""
        user_name = forms.ModelChoiceField(
             queryset=User.objects.filter(
                  is_active=True,
                  userprofile__bateponto="Sim"
             ).order_by("username"),
             label="Usuário",
             required=False,
        )
        month_choice = forms.ChoiceField(
             choices=get_previous_month_choices(),
             label='Selecione o mês',
             required=False,
             widget=forms.Select(attrs={
                  'class':'form-control',
             }),
             initial='',
        )


        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop("user_name", None)
            super(SearchFilterForm, self).__init__(*args, **kwargs)
            self.fields["month_choice"].initial = kwargs.get("initial", {}).get("month_choice", None)
            if self.user is not None:
                self.fields["user_name"].initial = self.user


class ConsultaValorInseridoForm(forms.Form):

     user_name = forms.ModelChoiceField(
          queryset=User.objects.filter(
               is_active=True,
               userprofile__bateponto="Sim"
          ).order_by("username"),
          label="Usuário",
          required=False,
          widget=forms.Select(attrs={
               'class':'select form-select',
          })
     )
     competencia = forms.ChoiceField(
             choices=get_previous_month_choices(),
             label='Selecione o mês',
             required=False,
             widget=forms.Select(attrs={
                  'class':'form-control',
             }),
             initial='',
        )


     def __init__(self, *args, **kwargs):
          self.user = kwargs.pop("user_name", None)
          super(ConsultaValorInseridoForm, self).__init__(*args, **kwargs)
          self.fields["competencia"].initial = kwargs.get("initial", {}).get("competencia", None)
          if self.user is not None:
               self.fields["user_name"].initial = self.user

class InserirValorForm(forms.ModelForm):

     pagamento_str = forms.DurationField(required=False, label="Pagamento em horas e minutos")
     compensacao_str = forms.DurationField(required=False, label="Compensação em horas e minutos")
     class Meta:
          model = ValorInserido
          fields = (
               'user',
               'competencia',
               'pagamento',
               'compensacao',

          )

     def __init__(self, *args, **kwargs):
          super(InserirValorForm, self).__init__(*args, **kwargs)

          # disable user and competencia fields
          self.fields["user"].disabled = True
          self.fields["competencia"].disabled = True
          self.fields["pagamento_str"].disabled = True
          self.fields["compensacao_str"].disabled = True

          # set initial value for pagamento
          if self.instance.pk:
               if self.instance.pagamento:
                    self.fields['pagamento_str'].initial = format_timedelta(self.instance.pagamento)
               else:
                    self.fields['pagamento_str'].initial = "00:00:00"
          else:
               self.fields['pagamento_str'].initial = "00:00:00"

          # set initial value for compensacao
          if self.instance.pk:
               if self.instance.compensacao:
                    self.fields['compensacao_str'].initial = format_timedelta(self.instance.compensacao)
               else:
                    self.fields['compensacao_str'].initial = "00:00:00"
          else:
               self.fields['compensacao_str'].initial = "00:00:00"

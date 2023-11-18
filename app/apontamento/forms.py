from django import forms
from django.contrib.auth.models import User
from apontamento.models import Ponto
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = "date"

class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

class FolhaPontoForm(forms.Form):
    entrada = forms.DateField(widget=DateInput, label="Início", required=True)
    saida = forms.DateField(widget=DateInput, label="Fim", required=True)
    usuario = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'), required=True)


    
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Ponto
        fields = ('entrada', 'primeiro', 'segundo', 'atraso', 'saida', 'usuario', 'fechado', 'cliente_id', 'tipo_receita', 'atrasoautorizado')
        widgets = {
            'entrada': DateTimeInput(),
            'saida': DateTimeInput(),
        }

    def __init__(self, *args, day=None, user_id=None, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.day = day
        self.user_id = user_id if user_id is not None else User.objects.filter(username=['usuario']).first().id
        # You can now use self.day and self.user_id in your form


class AppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Ponto
        fields = ('entrada', 'saida', 'usuario')
        widgets = {
            'entrada': DateTimeInput(),
            'saida': DateTimeInput(),
        }

    def __init__(self, *args, day=None, user_id=None, **kwargs):
        super(AppointmentUpdateForm, self).__init__(*args, **kwargs)
        self.day = day
        # self.user_id = user_id if user_id is not None else User.objects.filter(username=['usuario']).first().id
        # You can now use self.day and self.user_id in your form

        
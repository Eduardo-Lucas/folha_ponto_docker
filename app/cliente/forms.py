
from django import forms
import django_filters
from cliente.models import Cliente, ClienteTipoSenha, SituacaoEntidadeChoices, TipoDocumentoChoices


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nomerazao', 'codigosistema', 'tipodocumento', 'documento', 'situacaoentidade',
                  'inscricao_estadual', 'inscricao_municipal', 'inscricao_imobiliária',
                  'tributacao_municipal', 'tributacao_estadual', 'tributacao_federal',
                  'nire', 'observacao']

        labels = {
            'nomerazao': 'Nome Completo ou Razão Social',
            'codigosistema': 'Código',
            'tipodocumento': 'Tipo',
            'documento': 'Documento',
            'situacaoentidade': 'Situação',
            'observacao': 'Observação',

        }

        help_texts = {
            'nomerazao': 'Entre com o nome completo ou a Razão Social.',
            'tipodocumento': 'CPF ou CNPJ',
            'documento': 'Entre com o CNPJ ou CPF.',
            'codigosistema': 'Código',
            'situacaoentidade': 'Situação',

        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['situacaoentidade'].initial = 1
        # set a widget to the field tipodocumento
        if self.instance:
            self.fields['tipodocumento'].initial = 1 if len(str(self.instance.documento)) == 11 else 2
            # if len(codigo) <4 concatenate with zero in the left, else display codigo as it is
            self.fields['codigosistema'].initial = str(self.instance.codigosistema).zfill(4) if len(self.instance.codigosistema)<4 else self.instance.codigosistema


        self.fields['tipodocumento'].widget = forms.Select(choices=TipoDocumentoChoices.choices)

        self.fields['situacaoentidade'].widget = forms.Select(choices=SituacaoEntidadeChoices.choices)


class ClienteFilterForm(django_filters.FilterSet):
    class Meta:
        model = Cliente
        fields = {
            'nomerazao': ['icontains'],
            'codigosistema': ['icontains'],
        }

        labels = {
            'nomerazao': 'Razão Social',
            'codigosistema': 'Código',
        }

        help_texts = {
            'nomerazao': 'Entre com o nome completo ou a Razão Social.',
            'codigosistema': 'Código do sistema associado ao cliente.',
        }

class ClienteTipoSenhaForm(forms.ModelForm):
    class Meta:
        model = ClienteTipoSenha
        fields = ['tipo_senha', 'cliente', 'login', 'senha', 'informacao_adicional']

        labels = {
            'tipo_senha': 'Tipo de Senha',
            'cliente': 'Cliente',
            'login': 'Login',
            'senha': 'Senha',
            'informacao_adicional': 'Informação Adicional',
        }

        help_texts = {
            'tipo_senha': 'Informe o tipo de senha associado ao cliente.',
            'cliente': 'Informe o cliente associado a senha.',
            'login': 'Informe o login associado a senha.',
            'senha': 'Informe a senha associada ao cliente.',
            'informacao_adicional': 'Informe informações adicionais sobre a senha (Opcional).',
        }

    def __init__(self, *args, **kwargs):

        self.cliente_id = kwargs.pop('cliente_id', None)
        super(ClienteTipoSenhaForm, self).__init__(*args, **kwargs)

        if self.cliente_id:
            self.fields['cliente'].initial = Cliente.objects.get(id=self.cliente_id)
            # hidden field
            self.fields['cliente'].widget = forms.HiddenInput()
        else:
            self.fields['cliente'].initial = None

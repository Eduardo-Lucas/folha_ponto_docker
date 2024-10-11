
from django import forms
import django_filters
from cliente.models import Cliente, ClienteTipoSenha, TipoSenha


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nomerazao', 'codigosistema', 'documento', 'situacaoentidade',
                  'tipocertificado', 'senhacertificado', 'vencimentocertificado',
                  ]

        labels = {
            'nomerazao': 'Nome Completo ou Razão Social',
            'codigosistema': 'Código no Sistema',
            'documento': 'Documento',
            'situacaoentidade': 'Situação do Cliente',
            'tipocertificado': 'Tipo de Certificado',
            'senhacertificado': 'Senha do Certificado',
            'vencimentocertificado': 'Vencimento do Certificado',

        }

        help_texts = {
            'nomerazao': 'Entre com o nome completo ou a Razão Social.',
            'documento': 'Entre com o CNPJ ou CPF do cliente.',
            'codigosistema': 'Código do sistema associado ao cliente.',
            'situacaoentidade': 'Informe a situação do Cliente: 1 = Ativo.',
            'tipocertificado': 'Informe o tipo de certificado.',
            'senhacertificado': 'Informe a senha do certificado.',
            'vencimentocertificado': 'Informe a data de vencimento do certificado.',
        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['situacaoentidade'].initial = 1

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

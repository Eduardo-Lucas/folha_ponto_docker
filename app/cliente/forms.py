
from django import forms
from cliente.models import Cliente, ClienteTipoSenha


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nomerazao', 'codigosistema', 'situacaoentidade',
                  'tipocertificado', 'senhacertificado', 'vencimentocertificado',
                  ]

        labels = {
            'nomerazao': 'Nome Completo ou Razão Social',
            'codigosistema': 'Código no Sistema',
            'situacaoentidade': 'Situação do Cliente',
            'tipocertificado': 'Tipo de Certificado',
            'senhacertificado': 'Senha do Certificado',
            'vencimentocertificado': 'Vencimento do Certificado',

        }

        help_texts = {
            'nomerazao': 'Entre com o nome completo ou a Razão Social.',
            'codigosistema': 'Entre com o código do sistema associado ao cliente (Opcional).',
            'situacaoentidade': 'Informe a situação do Cliente: 1 = Ativo.',
            'tipocertificado': 'Informe o tipo de certificado.',
            'senhacertificado': 'Informe a senha do certificado.',
            'vencimentocertificado': 'Informe a data de vencimento do certificado.',
        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['situacaoentidade'].initial = 1


class ClienteTipoSenhaForm(forms.ModelForm):
    class Meta:
        model = ClienteTipoSenha
        fields = ['tipo_senha', 'cliente', 'login', 'senha', 'informacao_adicional']

        labels = {
            'tipo_senha': 'Tipo de Senha',
            'login': 'Login',
            'senha': 'Senha',
            'informacao_adicional': 'Informação Adicional',
        }

        help_texts = {
            'tipo_senha': 'Informe o tipo de senha associado ao cliente.',
            'login': 'Informe o login associado a senha.',
            'senha': 'Informe a senha associada ao cliente.',
            'informacao_adicional': 'Informe informações adicionais sobre a senha (Opcional).',
        }

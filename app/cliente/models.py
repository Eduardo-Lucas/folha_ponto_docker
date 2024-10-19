from django.db import models
import re

class ClienteManager(models.Manager):
    """Manager definition for Cliente."""

    def cliente_ativo(self):
        """Queryset definition for Cliente."""
        return super().get_queryset().filter(situacaoentidade=1)

    def cliente_inativo(self):
        """Queryset definition for Cliente."""
        # situacaoentidade not in 1
        return super().get_queryset().exclude(situacaoentidade=1)

    def get_queryset(self):
        """Queryset definition for Cliente."""
        return super().get_queryset().all()

class UpperCaseIntegerChoices(models.IntegerChoices):
    """Custom IntegerChoices to render labels in uppercase."""

    @classmethod
    def choices(cls):
        return [(key, value.upper()) for key, value in cls._member_map_.items()]

class TipoDocumentoChoices(UpperCaseIntegerChoices):
    """Choices definition for TipoDocumento."""

    CPF = 1
    CNPJ = 2
    OUTROS = 4

class SituacaoEntidadeChoices(UpperCaseIntegerChoices):
    """Choices definition for SituacaoEntidade."""

    ATIVADO = 1
    DESATIVADO = 2


class TipoSenha(models.Model):
    """Model definition for TipoSenha."""

    descricao = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.descricao

    class Meta:
        """Meta definition for TipoSenha."""

        ordering = ("descricao",)
        db_table = "tiposenha"
        verbose_name = "Tipo de Senha"
        verbose_name_plural = "Tipos de Senha"
class Cliente(models.Model):
    """Model definition for Cliente."""

    id = models.IntegerField(primary_key=True, auto_created=True)
    tipodocumento = models.IntegerField(
        null=True,
        blank=True,
        choices=TipoDocumentoChoices.choices,
        default=TipoDocumentoChoices.CPF,
    )
    documento = models.BigIntegerField(
        null=True,
        blank=True,
    )
    nomerazao = models.CharField(max_length=100)
    apelidofantazia = models.CharField(max_length=100)
    tipocertificado = models.IntegerField(
        null=True,
        blank=True,
    )
    senhacertificado = models.CharField(null=True, blank=True, max_length=50)
    vencimentocertificado = models.DateField(
        null=True,
        blank=True,
    )
    logositebv = models.BooleanField(
        null=True,
        blank=True,
    )
    iniciobv = models.DateField(
        null=True,
        blank=True,
    )
    observacao = models.CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    codigosistema = models.CharField(null=True, blank=True, max_length=10)
    situacaoentidade = models.IntegerField(null=True, blank=True, choices=SituacaoEntidadeChoices.choices, default=SituacaoEntidadeChoices.ATIVADO)
    codigoterceiro = models.CharField(
        null=True,
        blank=True,
        max_length=10,
    )
    controlarvencimentocertificado = models.BooleanField(default=False)
    emiteboleto = models.BooleanField(default=False)
    diavencimentoboleto = models.IntegerField(null=True, blank=True)
    grupoeconomico_id = models.CharField(
        null=True,
        blank=True,
        max_length=10,
    )

    telefone = models.CharField(max_length=20, null=True, blank=True)
    contato = models.CharField(max_length=50, null=True, blank=True)
    data_aniversario = models.DateField(null=True, blank=True)

    inscricao_estadual = models.CharField(max_length=20, null=True, blank=True, verbose_name="Inscrição Estadual")
    inscricao_imobiliária = models.CharField(max_length=20, null=True, blank=True, verbose_name="Inscrição Imobiliária")
    inscricao_municipal = models.CharField(max_length=20, null=True, blank=True, verbose_name="Inscrição Municipal")
    nire = models.CharField(max_length=20, null=True, blank=True, verbose_name="NIRE")
    tributacao_municipal = models.CharField(max_length=20, null=True, blank=True,  verbose_name="Tributação Municipal")
    tributacao_estadual = models.CharField(max_length=20, null=True, blank=True,   verbose_name="Tributação Estadual")
    tributacao_federal =  models.CharField(max_length=20, null=True, blank=True,   verbose_name="Tributação Federal")


    objects = ClienteManager()


    def save(self, *args, **kwargs):
        # take the max id and add 1 only if it is a new record
        if self.id is None:
            self.id = Cliente.objects.all().aggregate(models.Max("id"))["id__max"] + 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.codigosistema is not None:
            return "{0}|{1}".format(str(self.codigosistema).zfill(4), self.nomerazao)
        return self.nomerazao

    @property
    def get_codigosistema_formatado(self):
        if self.codigosistema:
            return self.codigosistema.zfill(4)
        else:
            return "-"

    def get_documento(self):
        if self.documento is not None:
            return self.documento
        else:
            return "-"

    @property
    def get_documento_cpf_cnpj(self):
        if self.documento is not None:
            if len(str(self.documento)) <= 11:
                cpf = str(self.documento).zfill(11)
                cpf_pontuado = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)
                return cpf_pontuado
            else:
                # formatar o CNPJ
                cnpj = str(self.documento).zfill(14)
                cnpj_pontuado = re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5', cnpj)
                return cnpj_pontuado

        else:
            return "-"

    @property
    def get_tipodocumento(self):
        # if length of documento is 11, then it is CPF, otherwise it is CNPJ
        if self.documento is not None:
            self.tipodocumento=1 if len(str(self.documento)) == 11 else 2
        # save
        self.save()

    class Meta:
        """Meta definition for Cliente."""

        ordering = ("nomerazao",)
        db_table = "clientes"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class ClienteTipoSenha(models.Model):
    """Model definition for ClienteTipoSenha."""

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_senha = models.ForeignKey(TipoSenha, on_delete=models.CASCADE)
    login = models.CharField(max_length=50, null=True, blank=True)
    senha = models.CharField(max_length=50, null=True, blank=True)
    informacao_adicional = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.tipo_senha} - {self.cliente}"

    def get_login(self):
        if self.login:
            return self.login
        else:
            return "-"

    def get_senha(self):
        if self.senha:
            return self.senha
        else:
            return "-"
    def get_informacao_adicional(self):
        if self.informacao_adicional:
            return self.informacao_adicional
        else:
            return "-"

    class Meta:
        """Meta definition for ClienteTipoSenha."""

        db_table = "cliente_tipo_senha"
        verbose_name = "Cliente Tipo Senha"
        verbose_name_plural = "Clientes Tipos Senhas"

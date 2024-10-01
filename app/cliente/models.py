from django.db import models


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


class TipoSenha(models.Model):
    """Model definition for TipoSenha."""

    descricao = models.CharField(max_length=50)

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
    situacaoentidade = models.IntegerField(null=True, blank=True)
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
    contato_id = models.IntegerField(null=True, blank=True)




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

    def get_codigosistema_formatado(self):
        if self.codigosistema:
            return self.codigosistema.zfill(4)
        else:
            return "-"


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
    login = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    informacao_adicional = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.tipo_senha} - {self.cliente}"
    class Meta:
        """Meta definition for ClienteTipoSenha."""

        db_table = "cliente_tipo_senha"
        verbose_name = "Cliente Tipo Senha"
        verbose_name_plural = "Clientes Tipos Senhas"

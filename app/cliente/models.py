from django.db import models


class ClienteManager(models.Manager):
    """Manager definition for Cliente."""

    def cliente_ativo(self):
        """Queryset definition for Cliente."""
        return super().get_queryset().filter(situacaoentidade=1)

    def get_queryset(self):
        """Queryset definition for Cliente."""
        return super().get_queryset().all()


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
    controlarvencimentocertificado = models.BooleanField()
    emiteboleto = models.BooleanField()
    diavencimentoboleto = models.IntegerField(null=True, blank=True)
    grupoeconomico_id = models.CharField(
        null=True,
        blank=True,
        max_length=10,
    )
    contato_id = models.IntegerField(null=True, blank=True)

    objects = ClienteManager()

    def __str__(self) -> str:
        if self.codigosistema is not None:
            return "{0}|{1}".format(str(self.codigosistema).zfill(4), self.nomerazao)
        return self.nomerazao

    class Meta:
        """Meta definition for Cliente."""

        ordering = ("nomerazao",)
        db_table = "clientes"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

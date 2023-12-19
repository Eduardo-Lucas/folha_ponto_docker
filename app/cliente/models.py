from django.db import models


class Cliente(models.Model):
    '''Model definition for Cliente.'''
    id = models.IntegerField(primary_key=True)
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
        null=True, blank=True, max_length=10,
    )
    controlarvencimentocertificado = models.BooleanField()
    emiteboleto = models.BooleanField()
    diavencimentoboleto = models.IntegerField(null=True, blank=True)
    grupoeconomico_id = models.DecimalField(
        null=True,
        blank=True,
        decimal_places=1,
        max_digits=10,
    )
    contato_id = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return "{0}|{1}".format(str(self.codigosistema).zfill(4), self.nomerazao)

    class Meta:
        '''Meta definition for Cliente.'''
        ordering = ("nomerazao",)
        db_table = "clientes"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

""" Models para o app banco_de_horas."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


class BancoDeHorasManager(models.Manager):
    """ " Manager customizado para o model BancoDeHoras."""

    # check if there is banco de horas for the user in the period
    def check_banco_de_horas_existente(self, periodo):
        """Verifica se existe banco de horas para um determinado período."""
        return self.filter(periodo_apurado=periodo).exists()

    def remover_todas_horas(self, periodo):
        """Remove todas as horas do banco de horas de todos os usuários
        em um determinado período."""
        BancoDeHoras.objects.filter(periodo_apurado=periodo).delete()

    def consultar_saldo(self, user_id, periodo):
        """Consulta o saldo de horas de um usuário em um determinado período."""
        banco_de_horas = self.filter(user_id=user_id, periodo_apurado=periodo).first()

        if banco_de_horas:
            return banco_de_horas.saldo_final_com_pagamento
        return timedelta(hours=0, minutes=0, seconds=0)


class ValorInserido(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competencia = models.DateField()
    compensacao = models.DurationField(default=timedelta(hours=0, minutes=0, seconds=0))
    pagamento = models.DurationField(default=timedelta(hours=0, minutes=0, seconds=0))

    class Meta:

        ordering = (
            '-competencia',
            'user',
        )
        db_table = 'valor_inserido'
        unique_together = ("user", "competencia")
        verbose_name = 'Valor Inserido'
        verbose_name_plural = 'Valores Inseridos'


    def __str__(self):
        return f"Valor Inserido - Usuário: {self.user.username} - Competência: {self.competencia} - Pagamento: {self.pagamento} - Compensacao: {self.compensacao}"


class BancoDeHoras(models.Model):
    """Model para o banco de horas dos usuários."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    periodo_apurado = models.DateField()
    total_credor = models.DurationField(
        default=timedelta(hours=0, minutes=0, seconds=0)
    )

    total_devedor = models.DurationField(
        default=timedelta(hours=0, minutes=0, seconds=0)
    )
    saldo_anterior = models.DurationField(
        default=timedelta(hours=0, minutes=0, seconds=0)
    )
    compensacao = models.DurationField(default=timedelta(hours=0, minutes=0, seconds=0))
    pagamento = models.DurationField(default=timedelta(hours=0, minutes=0, seconds=0))


    objects = BancoDeHorasManager()

    class Meta:
        """Meta class para o model BancoDeHoras."""

        ordering = (
            "-periodo_apurado",
            "user",

        )
        db_table = "banco_de_horas"
        unique_together = ("user", "periodo_apurado")
        verbose_name = "Banco de Horas"
        verbose_name_plural = "Bancos de Horas"

    def __str__(self):
        return f"Banco de horas - Usuário: {self.user.username}, Período: {self.periodo_apurado}"

    @property
    def saldo_final_sem_pagamento(self):
        """Calcula o saldo final de horas sem o pagamento."""
        return (
            self.total_credor
            - self.total_devedor
            + self.saldo_anterior
            + self.compensacao
        )

    @property
    def saldo_final_com_pagamento(self):
        """Calcula o saldo final de horas."""
        if self.pagamento is None:
            self.pagamento = timedelta(hours=0, minutes=0, seconds=0)
        else:
            self.pagamento = self.pagamento

        return self.saldo_final_sem_pagamento - self.pagamento

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Ferias(models.Model):
    """Model definition for Ferias."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ferias")
    periodo = models.IntegerField(
        default=2023,
        validators=[MinValueValidator(2020)],
    )
    data_inicial = models.DateField()
    data_final = models.DateField()
    cumpriu = models.BooleanField(default=False)
    cadastrado_em = models.DateTimeField(
        auto_now_add=True
    )  # auto_now_add=True -> Salva a data atual quando o objeto é criado

    def __str__(self):
        """Unicode representation of Ferias."""
        return f"{self.user.username} - {self.periodo}"

    @property
    def status_ferias(self):
        """Retorna o status das férias."""
        if self.cumpriu:
            return "Sim"
        return "Não"

    @property
    def dias_corridos(self):
        """Retorna a quantidade de dias corridos."""
        return (self.data_final - self.data_inicial).days + 1

    @property
    def saldo_dias(self):
        """Retorna o saldo de dias de férias."""
        return 20 - self.dias_corridos

    class Meta:
        """Meta definition for Ferias."""

        ordering = [
            "-periodo",
        ]
        verbose_name = "Férias"
        verbose_name_plural = "Férias"
        db_table = "ferias"
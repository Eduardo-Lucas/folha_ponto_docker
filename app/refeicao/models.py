"""
 Controle de Refeições
"""

from django.contrib.auth.models import User
from django.db import models


class RefeicaoManager(models.Manager):
    """Manager para controle de refeições"""

    def get_queryset(self):
        """Retorna queryset de refeições"""
        return super().get_queryset().all()

    def get_queryset_consumo(self):
        """Retorna queryset de refeições"""
        return super().get_queryset().filter(consumo=False)

    def get_queryset_usuario(self, usuario):
        """Retorna queryset de refeições"""
        return super().get_queryset().filter(usuario=usuario)

    def get_queryset_usuario_consumo_verdadeiro(self, usuario):
        """Retorna queryset de refeições"""
        return super().get_queryset().filter(usuario=usuario, consumo=True)

    def get_queryset_usuario_consumo_falso(self, usuario):
        """Retorna queryset de refeições"""
        return super().get_queryset().filter(usuario=usuario, consumo=False)

    def get_queryset_data(self, data_refeicao):
        """Retorna queryset de refeições"""
        return super().get_queryset().filter(data_refeicao=data_refeicao)

    def get_queryset_data_consumo_verdadeiro(self, data_refeicao):
        """Retorna queryset de refeições"""
        return super().get_queryset().filter(data_refeicao=data_refeicao, consumo=True)

    def get_queryset_data_consumo_falso(self, data_refeicao):
        """Retorna queryset de refeições"""
        return super().get_queryset().filter(data_refeicao=data_refeicao, consumo=False)

    def get_queryset_usuario_data(self, usuario, data_refeicao):
        """Retorna queryset de refeições"""
        return (
            super().get_queryset().filter(usuario=usuario, data_refeicao=data_refeicao)
        )

    def get_queryset_usuario_data_consumo_verdadeiro(self, usuario, data_refeicao):
        """Retorna queryset de refeições"""
        return (
            super()
            .get_queryset()
            .filter(usuario=usuario, data_refeicao=data_refeicao, consumo=True)
        )

    def get_queryset_usuario_data_consumo_falso(self, usuario, data_refeicao):
        """Retorna queryset de refeições"""
        return (
            super()
            .get_queryset()
            .filter(usuario=usuario, data_refeicao=data_refeicao, consumo=False)
        )


class Refeicao(models.Model):
    """Class paara controle de refeições"""

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_refeicao = models.DateField()
    consumo = models.BooleanField(default=True)
    observacao = models.TextField(blank=True)

    objects = RefeicaoManager()

    @property
    def get_consumo(self):
        """Retorna consumo"""
        return "Sim" if self.consumo else "Não"

    def __str__(self):
        return f"{self.usuario} - {self.data_refeicao} - {self.get_consumo}"

    class Meta:
        """Meta options"""

        ordering = ["-data_refeicao"]
        unique_together = ["usuario", "data_refeicao"]
        db_table = "refeicao"
        verbose_name = "Refeição"
        verbose_name_plural = "Refeições"

    def get_consumo_display(self):
        """Retorna consumo"""
        return "Sim" if self.consumo else "Não"

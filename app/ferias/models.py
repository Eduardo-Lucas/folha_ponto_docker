from datetime import datetime, timedelta

import numpy as np
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from feriado.models import Feriado
from folha_ponto.settings import FERIAS_BUSINESS_DAYS  # 20 Days


class FeriasManager(models.Manager):
    """Manager for Ferias."""

    def get_ferias(self, data_inicial=None, data_final=None, user=None):
        """Get ferias within the range of date for an user
        Return the days of the period that the user is on vacation
        """
        if data_inicial and data_final and user:

            # query the days within the range of a given date
            query = self.filter(
                user=user,
                data_inicial__lte=data_final,
                data_final__gte=data_inicial,
            )

            if query:
                return "Sim"
            return "Não"

    def get_proximas_ferias(self):
        """Get the next vacation period"""
        # query the begining ot the current month

        return self.filter(data_final__gte=datetime.now().date()).order_by(
            "data_inicial"
        )

    def get_ferias_anteriores(self, data_inicial=None, data_final=None, user=None):
        """Get the previous vacation period"""
        query = self.filter(
            periodo=data_inicial.year, user=user, data_inicial__lt=data_inicial
        )
        # sum dias_uteis from query
        dias_uteis = sum(ferias.get_dias_uteis for ferias in query)

        # Subtract the number of holidays from the total number of days
        return dias_uteis



class Ferias(models.Model):
    """Model definition for Ferias."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ferias")
    periodo = models.IntegerField(
        default=2023,
        validators=[MinValueValidator(2020)],
    )
    data_inicial = models.DateField()
    data_final = models.DateField()
    dias_uteis = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(FERIAS_BUSINESS_DAYS)],
    )
    cumpriu = models.BooleanField(default=False)
    cadastrado_em = models.DateTimeField(
        auto_now_add=True
    )  # auto_now_add=True -> Salva a data atual quando o objeto é criado

    objects = FeriasManager()

    class Meta:
        """Meta definition for Ferias."""

        ordering = [
            "user",
            "periodo",
            "data_inicial",
        ]
        verbose_name = "Férias"
        verbose_name_plural = "Férias"
        db_table = "ferias"

    def __str__(self):
        """Unicode representation of Ferias."""
        return f"{self.user.username} - {self.periodo} - {self.data_inicial} - {self.data_final}"

    @property
    def status_ferias(self):
        """Retorna o status das férias."""
        if self.cumpriu:
            return "Sim"
        return "Não"

    @property
    def get_dias_uteis(self):
        """Retorna os dias úteis de férias."""

        dias_uteis = np.busday_count(
            self.data_inicial, self.data_final
        )
        feriados = Feriado.objects.get_how_many_holidays(
            self.data_inicial, self.data_final
        )

        return (dias_uteis +1) - feriados

    @property
    def saldo_dias(self):
        """Retorna o saldo de dias de férias."""
        saldo_anterior = Ferias.objects.get_ferias_anteriores(
            data_inicial=self.data_inicial,
            data_final=self.data_final,
            user=self.user
        )
        saldo = FERIAS_BUSINESS_DAYS - saldo_anterior - self.get_dias_uteis

        return saldo

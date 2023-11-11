from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time, timedelta, timezone 
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User


class PontoManager(models.Manager):
    """
    Manager for the Ponto model.
    """
    def for_day(self, day=None, user=None):
        """
        Returns all Ponto objects for a given day and user.
        """
        if day is None:
            day = timezone.now().date()
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        return self.filter(entrada__range=(start, end), usuario=user)

    def get_open_pontos(self, user=None):
        """
        Returns all open Ponto objects for a given user.
        """
        return self.filter(usuario=user, fechado=False)




class Ponto(models.Model):
    """
    Model to represent a point in time for a user.
    """
    id = models.IntegerField(primary_key=True)
    entrada = models.DateTimeField()
    primeiro = models.BooleanField(default=False)
    segundo = models.BooleanField(default=False)
    atraso = models.BooleanField(default=False)
    saida = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fechado = models.BooleanField(default=False)
    cliente_id = models.IntegerField(null=True, blank=True)
    tiporeceita_id = models.IntegerField(null=True, blank=True)
    atrasoautorizado = models.BooleanField(default=False)

    objects = PontoManager()

    class Meta:
        """
        Metadata for the Ponto model.
        """
        ordering = ("entrada",)
        db_table = "pontos"
        verbose_name = "Ponto"
        verbose_name_plural = "Pontos"

    @property
    def difference(self):
        """
        Calculates the difference between the entry and exit times.
        """
        if self.saida is not None:
            return self.saida - self.entrada
        return timedelta(0)

    def __str__(self) -> str:
        """
        Returns a string representation of the Ponto object.
        """
        return f"{self.usuario} {self.entrada} {self.saida} {self.difference}"

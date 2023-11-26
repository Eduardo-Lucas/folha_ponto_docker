from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time, timedelta, timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cliente.models import Cliente

class TipoReceita(models.Model):
    RECIBO_CHOICES = (
        (True, 'Sim'),
        (False, 'Não'),
    )
    STATUS_CHOICES = (
        (True, 'Ativo'),
        (False, 'Inativo'),
    )
    id = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=100)
    recibo = models.BooleanField(
        choices=RECIBO_CHOICES,
        default=False,
    )
    status = models.BooleanField(
        choices=STATUS_CHOICES,
        default=True,
    )

    class Meta:
        """
        Metadata for the TipoReceita model.
        """
        ordering = ("descricao",)
        db_table = "tiporeceitas"
        verbose_name = "Tipo de Receita"
        verbose_name_plural = "Tipos de Receitas"

    def __str__(self):
        return str(self.descricao)

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
    atraso = models.BooleanField(default=False, verbose_name="Atraso")
    saida = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fechado = models.BooleanField(default=False)
    cliente_id = models.ForeignKey(Cliente,
                                   on_delete=models.CASCADE,
                                   verbose_name="Cliente",
                                   null=True,
                                   blank=True)
    tipo_receita = models.ForeignKey(TipoReceita,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)
    atrasoautorizado = models.BooleanField(default=False, verbose_name="Atraso Autorizado")

    objects = PontoManager()

    class Meta:
        """
        Metadata for the Ponto model.
        """
        ordering = ("entrada", )
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

    @property
    def cliente(self):
        """
        Returns the client for the Ponto object.
        """
        if self.cliente_id is not None:
            return self.cliente_id
        return '-'

    def get_absolute_url(self):
        """ Returns the url to access a particular instance of the model."""
        return reverse('apontamento:appointment_detail', args=[self.id])

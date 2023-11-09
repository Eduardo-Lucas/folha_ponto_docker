from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta 

class Ponto(models.Model):
    id = models.IntegerField(
        primary_key=True,
    )
    entrada = models.DateTimeField()
    primeiro = models.BooleanField(default=False)
    segundo = models.BooleanField(default=False)
    atraso = models.BooleanField(default=False)
    saida = models.DateTimeField(null=True, blank=True)
    usuario= models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fechado = models.BooleanField(default=False)
    cliente_id = models.IntegerField(null=True, blank=True)
    tiporeceita_id = models.IntegerField(null=True, blank=True)
    atrasoautorizado = models.BooleanField(default=False)

    class Meta:
        ordering = ("entrada",)
        db_table = "pontos"
        verbose_name = "Ponto"
        verbose_name_plural = "Pontos"

    
    @property
    def difference(self):
        if self.saida is not None:
            return self.saida - self.entrada
        return timedelta(0)
        
    def __str__(self) -> str:
        return f"{self.usuario} {self.entrada} {self.saida} {self.difference}"


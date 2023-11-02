from django.db import models


class Feriado(models.Model):
    id = models.IntegerField(primary_key=True)
    dia = models.IntegerField()
    month = models.IntegerField()
    ano = models.IntegerField(default=0)
    descricao = models.CharField(max_length=100)
    fixo = models.BooleanField()
    situacaoentidade = models.IntegerField()
    importado = models.BooleanField()

    def __str__(self) -> str:
        return f"{str(self.id).zfill(4)}:{self.descricao}"

    class Meta:
        ordering = ("descricao",)
        db_table = "feriados"
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"

from django.db import models


class FeriadoManager(models.Manager):
    """
    Manager for the Feriado model.
    """

    def is_holiday(self, year=None, month=None, day=None):
        """
        Returns True if the given day is a holiday.
        """
        feriado = self.filter(dia=day, month=month, fixo=True).exists()
        if feriado:
            return True

        feriado = self.filter(dia=day, month=month, ano=year).exists()
        if feriado:
            return True

        return False

    def get_description(self, year=None, month=None, day=None):
        """
        Returns the description of the given holiday.
        """
        feriado = self.filter(dia=day, month=month, fixo=True).exists()
        if feriado:
            return self.filter(dia=day, month=month).first().descricao

        feriado = self.filter(dia=day, month=month, ano=year).exists()
        if feriado:
            return self.filter(dia=day, month=month, ano=year).first().descricao

        return None


class Feriado(models.Model):
    """
    Model for the Feriado entity.
    """

    id = models.AutoField(primary_key=True)
    dia = models.IntegerField()
    month = models.IntegerField()
    ano = models.IntegerField(default=0)
    descricao = models.CharField(max_length=100)
    fixo = models.BooleanField()
    situacaoentidade = models.IntegerField()
    importado = models.BooleanField()

    objects = FeriadoManager()

    def __str__(self) -> str:
        return f"{str(self.id).zfill(4)}:{self.descricao}"

    class Meta:
        """Metadata for the Feriado model."""

        ordering = ("descricao",)
        db_table = "feriados"
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"

from datetime import timedelta
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

    def get_how_many_holidays(self, data_inicial, data_final):
        """Returns the number of holidays between the given dates"""
        # if it is a fixed holiday, it will be repeated every year and we can use the month and day to filter
        fixed_holiday = self.filter(
            fixo=True,
            month__range=(data_inicial.month, data_final.month),
            dia__range=(data_inicial.day, data_final.day),

        ).count()

        # if it is not a fixed holiday, we need to filter by the year
        non_fixed_holiday = self.filter(
            fixo=False,
            ano__range=(data_inicial.year, data_final.year),
            month__range=(data_inicial.month, data_final.month),
            dia__range=(data_inicial.day, data_final.day),
        ).count()

        return fixed_holiday + non_fixed_holiday

    def get_lista_dias_uteis(self, data_inicial, data_final):
        """Returns a list with the business days between the given dates"""
        dias_uteis = []
        data = data_inicial
        while data <= data_final:
            if data.weekday() < 5 and not self.is_holiday(data.year, data.month, data.day):
                dias_uteis.append(data)
            data += timedelta(days=1)
        return dias_uteis


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
        if self.fixo:
            return f"{self.dia}/{self.month} - {str(self.id).zfill(4)}:{self.descricao}"
        return f"{self.dia}/{self.month}/{self.ano} - {str(self.id).zfill(4)}:{self.descricao}"


    class Meta:
        """Metadata for the Feriado model."""

        ordering = ("descricao",)
        db_table = "feriados"
        verbose_name = "Feriado"
        verbose_name_plural = "Feriados"

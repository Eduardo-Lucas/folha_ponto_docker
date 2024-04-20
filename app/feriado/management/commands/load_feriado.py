import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from feriado.models import Feriado


class Command(BaseCommand):
    """Load Feriado from a CSV file."""

    help = "Loads Feriado."

    def handle(self, *args, **options):
        load_data_from_csv()


def load_data_from_csv():
    """Load data from csv file."""
    with open("Feriado-2024-04-20.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:

            obj = Feriado(
                id=row["id"],
                dia=row["dia"],
                month=row["month"],
                ano=row["ano"],
                descricao=row["descricao"],
                fixo=row["fixo"],
                situacaoentidade=row["situacaoentidade"],
                importado=row["importado"],
            )

            obj.save()
        print("Feriados have been successfully uploaded.")

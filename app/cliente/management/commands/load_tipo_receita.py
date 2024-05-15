import csv

from apontamento.models import TipoReceita
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Load TipoReceita from a CSV file."""

    help = "Loads TipoReceita."

    def handle(self, *args, **options):
        load_data_from_csv()


def load_data_from_csv():
    """Load data from csv file."""
    with open("TipoReceita-2024-05-10.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:

            obj = TipoReceita(
                id=row["id"],
                descricao=row["descricao"],
                recibo=row["recibo"],
                status=row["status"],
            )
            obj.save()
        print("Tipo Receita have been successfully uploaded.")

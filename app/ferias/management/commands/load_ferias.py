import csv
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from ferias.models import Ferias


class Command(BaseCommand):
    """Load Ferias from a CSV file."""

    help = "Loads Ferias."

    def handle(self, *args, **options):
        load_data_from_csv()


def load_data_from_csv():
    """Load data from csv file."""
    with open("Ferias-current.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:

            obj = Ferias(
                id=row["id"],
                user=User.objects.get(id=row["user"]),
                periodo=row["periodo"],
                data_inicial=row["data_inicial"],
                data_final=row["data_final"],
                dias_uteis=row["dias_uteis"],
                cumpriu=row["cumpriu"],
                cadastrado_em=row["cadastrado_em"],
            )

            obj.save()
        print("Ferias have been successfully uploaded.")

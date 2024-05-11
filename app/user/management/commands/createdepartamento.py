import csv

from django.core.management.base import BaseCommand
from user.models import Departamento


class Command(BaseCommand):
    help = "Reads a CSV file and inserts data into Departamento model"

    def handle(self, *args, **options):
        with open("Departamento-2024-05-10.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Departamento.objects.create(
                    id=row["id"],
                    nome=row["nome"],
                )

            print("Departamentos have been successfully created.")

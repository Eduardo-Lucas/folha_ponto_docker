
import csv
from datetime import datetime

from apontamento.models import Ponto, TipoReceita
from cliente.models import Cliente
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Load Ponto from a CSV file."""

    help = "Loads Ponto."

    def handle(self, *args, **options):
        populate_pontos_from_csv()


def populate_pontos_from_csv():
    """Populate Ponto from a CSV file."""
    with open("Ponto-current.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # next(csv_reader)  # Skip the header row
        contador = 0
        print("Processing Ponto upload...")
        for row in csv_reader:
            initial_time = datetime.now()

            # only prints if contador is multiple of 1000
            if contador % 1000 == 0:
                print(f"Processing contador {contador}...")

            if row["saida"]:
                saida_fmt = row["saida"]
            else:
                saida_fmt = None

            usuario_var = User.objects.get(id=row["usuario"])

            if row["cliente_id"]:
                cliente_var = Cliente.objects.get(id=row["cliente_id"])
            else:
                cliente_var = None

            tipo_receita_var = TipoReceita.objects.get(id=row["tipo_receita"])

            ponto_id = int(row["id"])
            entrada = row["entrada"]
            primeiro = row["primeiro"]
            segundo = row["segundo"]
            atraso = row["atraso"]
            saida = saida_fmt
            usuario = usuario_var
            fechado = row["fechado"]
            cliente_id = cliente_var
            tipo_receita = tipo_receita_var
            atrasoautorizado = row["atrasoautorizado"]
            over_10_hours_authorization = row["over_10_hours_authorization"]

            # Create a new Ponto object and save it to the database
            ponto = Ponto(
                id=ponto_id,
                entrada=entrada,
                primeiro=primeiro,
                segundo=segundo,
                atraso=atraso,
                saida=saida,
                usuario=usuario,
                fechado=fechado,
                cliente_id=cliente_id,
                tipo_receita=tipo_receita,
                atrasoautorizado=atrasoautorizado,
                over_10_hours_authorization=over_10_hours_authorization,
            )
            ponto.save()
            contador += 1

    final_time = datetime.now()
    time_diff = final_time - initial_time
    # time_diff formatted in hours, minutes and seconds
    total_seconds = time_diff.total_seconds()
    print(f"Processing time: {total_seconds}")
    print(f"{contador} Pontos have been successfully uploaded.")

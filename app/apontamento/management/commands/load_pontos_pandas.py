import csv
from datetime import datetime, time, timedelta

import pandas as pd
import pytz
from apontamento.models import Ponto, TipoReceita
from cliente.models import Cliente
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Load Ponto from a CSV file."""

    help = "Loads Ponto."

    def handle(self, *args, **options):
        load_data_from_csv()


def load_data_from_csv():
    """Load data from csv file."""
    df = pd.read_csv("Ponto-2024-04-20.csv")

    # pontos = []
    for index, row in df.iterrows():
        cliente = (
            Cliente.objects.get(id=row["cliente_id"])
            if row["cliente_id"] and str(row["cliente_id"]).isdigit()
            else None
        )

        # Split the line into multiple lines for better readability
        # tipo_receita = (
        #     TipoReceita.objects.get(id=pd.to_numeric(row['tiporeceita_id']))
        #     if row['tiporeceita_id']
        #     else None
        # )
        tipo_receita = None

        if pd.notnull(row["saida"]):
            saida = pd.to_datetime(
                str(row["saida"]).split(".", maxsplit=1)[0], format="%Y-%m-%d %H:%M:%S"
            )
        else:
            saida = None

        entrada = pd.to_datetime(
            str(row["entrada"]).split(".", maxsplit=1)[0], format="%Y-%m-%d %H:%M:%S"
        )
        ponto = Ponto(
            id=row["id"],
            entrada=entrada,
            primeiro=row["primeiro"],
            segundo=row["segundo"],
            atraso=row["atraso"],
            saida=saida,
            usuario=(
                User.objects.get(id=row["usuario_id"]) if row["usuario_id"] else None
            ),
            fechado=row["fechado"],
            cliente_id=cliente,
            tipo_receita=tipo_receita,
            atrasoautorizado=row["atrasoautorizado"],
        )
        ponto.save()
        # pontos.append(ponto)

    # Ponto.objects.bulk_create(pontos)
    print("Pontos-2023 have been successfully uploaded using pandas.")

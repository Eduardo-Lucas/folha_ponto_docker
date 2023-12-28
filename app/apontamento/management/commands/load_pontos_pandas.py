import csv
from datetime import datetime, timezone
import pytz
from apontamento.models import Ponto, TipoReceita
from cliente.models import Cliente
from django.core.management.base import BaseCommand
import pandas as pd

class Command(BaseCommand):
    '''Load Ponto from a CSV file.'''
    help = 'Loads Ponto.'

    def handle(self, *args, **options):
        load_data_from_csv()

def load_data_from_csv():
    """ Load data from csv file."""
    df = pd.read_csv('Pontos-2023.csv')

    pontos = []
    for index, row in df.iterrows():

        if pd.notnull(row['saida']):
            saida = pd.to_datetime(row['saida']).tz_localize('UTC')
        else:
            saida = None

        try:
            cliente = Cliente.objects.get(id=row['cliente_id'])
        except Cliente.DoesNotExist:
            cliente = None

        ponto = Ponto(saida=saida, cliente=cliente, ...)
        pontos.append(ponto)

    Ponto.objects.bulk_create(pontos)

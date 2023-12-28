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

        try:
            tipo_receita=TipoReceita.objects.get(id=row['tipo_receita_id'])
        except TipoReceita.DoesNotExist:
            tipo_receita = None

        ponto = Ponto(id=row['id'],
                      entrada=datetime.strptime(row['entrada'].split('.')[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC),
                      primeiro=row['primeiro'],
                      segundo=row['segundo'],
                      atraso=row['atraso'],
                      saida=saida,
                      usuario=row['usuario'],
                      fechado=row['fechado'],
                      cliente_id=cliente,
                      tipo_receita=tipo_receita,
                      atrasoautorizado=row['atrasoautorizado']
                    )
        pontos.append(ponto)

    Ponto.objects.bulk_create(pontos)
    print("Pontos-2023 have been successfully uploaded using pandas.")

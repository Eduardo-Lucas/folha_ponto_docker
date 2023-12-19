import csv
from datetime import datetime, timezone
import pytz
from apontamento.models import Ponto, TipoReceita
from cliente.models import Cliente
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''Load Ponto from a CSV file.'''
    help = 'Loads Ponto.'

    def handle(self, *args, **options):
        load_data_from_csv()

def load_data_from_csv():
    """ Load data from csv file."""
    with open('Pontos-2023.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            if row['saida']:
                saida = datetime.strptime(row['saida'].split('.')[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC)
            else:
                saida = None

            try:
                cliente=Cliente.objects.get(id=row['cliente_id'])
            except Cliente.DoesNotExist:
                cliente = None

            try:
                tipo_receita=TipoReceita.objects.get(id=row['tipo_receita_id'])
            except TipoReceita.DoesNotExist:
                tipo_receita = None

            obj = Ponto(
                id=row['id'],
                entrada=datetime.strptime(row['entrada'].split('.')[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.UTC),
                primeiro=row['primeiro'],
                segundo=row['segundo'],
                atraso=row['atraso'],
                saida=saida,
                usuario=row['usuario'],
                fechado=row['fechado'],
                cliente_id=cliente,
                tipo_receita=tipo_receita,
                atrasoautorizado=row['atrasoautorizado'],
            )
            obj.save()
        print("Pontos-2023 have been successfully uploaded.")

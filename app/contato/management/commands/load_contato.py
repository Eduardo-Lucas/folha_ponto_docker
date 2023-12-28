import csv
from contato.models import Contato
from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    '''Load Contato from a CSV file.'''
    help = 'Loads Contato.'

    def handle(self, *args, **options):
        load_data_from_csv()

def load_data_from_csv():
    """ Load data from csv file."""
    with open('Contato.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            cargo_id = int(float(row['cargo_id'])) if row['cargo_id'] else None
            nascimento = datetime.strptime(row['nascimento'], '%Y-%m-%d') if row['nascimento'] else None

            obj = Contato(
                id=row['id'],
                cpf=row['cpf'],
                nome=row['nome'],
                observation=row['observation'],
                situacaoentidade=row['situacaoentidade'],
                cargo_id=cargo_id,
                nascimento=nascimento,
            )

            obj.save()
        print("Contatos have been successfully uploaded.")

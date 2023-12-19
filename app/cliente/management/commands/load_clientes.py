import csv
from cliente.models import Cliente
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''Load Cliente from a CSV file.'''
    help = 'Loads Cliente.'

    def handle(self, *args, **options):
        load_data_from_csv()

def load_data_from_csv():
    """ Load data from csv file."""
    with open('Cliente.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            obj = Cliente(
                id=row['id'],
                tipodocumento=row['tipodocumento'],
                documento=row['documento'],
                nomerazao=row['nomerazao'],
                apelidofantazia=row['apelidofantazia'],
                tipocertificado=row['tipocertificado'],
                senhacertificado=row['senhacertificado'],
                vencimentocertificado=row['vencimentocertificado'],
                logositebv=row['logositebv'],
                iniciobv=row['iniciobv'],
                observacao=row['observação'],
                codigosistema=row['codigosistema'],
                situacaoentidade=row['situacaoentidade'],
                codigoterceiro=row['codigoterceiro'],
                controlarvencimentocertificado=row['controlarvencimentocertificado'],
                emiteboleto=row['emiteboleto'],
                diavencimentoboleto=row['diavencimentoboleto'],
                grupoeconomico_id=row['grupoeconomico_id'],
                contato_id=row['contato_id'],
            )
            obj.save()
        print("Clientes have been successfully uploaded.")

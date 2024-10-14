import csv
from django.core.management.base import BaseCommand
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Update documento field in CSV file with database IDs'

    def handle(self, *args, **kwargs):
        input_file = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/ClienteTipoSenha-2024-10-14 - Clientes não encontrados.csv'
        output_file = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/Updated_ClienteTipoSenha-2024-10-14 - Clientes não encontrados.csv'

        with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                nomerazao = row['nomerazao']
                try:
                    cliente = Cliente.objects.filter(nomerazao=nomerazao).first()
                    row['cliente'] = cliente.id
                except Cliente.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Cliente with Nome {nomerazao} not found.'))
                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS('CSV file has been updated successfully.'))

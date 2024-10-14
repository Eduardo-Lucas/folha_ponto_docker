import csv
from django.core.management.base import BaseCommand
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Ajusta clientes não encontrados'

    def handle(self, *args, **kwargs):
        file_path = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/ClienteTipoSenha-2024-10-14 - Clientes não encontrados.csv'

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                nomerazao = row['nomerazao']
                documento = row['documento']

                cliente, created = Cliente.objects.get_or_create(nomerazao=nomerazao)
                cliente.documento = documento
                cliente.save()

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new cliente: {nomerazao}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated cliente: {nomerazao}'))

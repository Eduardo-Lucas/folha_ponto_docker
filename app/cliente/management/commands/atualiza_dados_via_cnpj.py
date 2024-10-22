import csv
from django.core.management.base import BaseCommand
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Atualiza dados via CNPJ'

    def handle(self, *args, **kwargs):
        file_path = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/bv-clientes-documentos - sheet1.csv'

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cnpj_cpf = row['cnpj_cpf']
                descricao = row['DESCRICAO']
                numero = row['NUMERO']


                try:
                    cliente = Cliente.objects.filter(documento=cnpj_cpf).first()

                    if descricao == 'Inscrição Municipal':
                        cliente.inscricao_municipal = numero
                    elif descricao == 'Inscrição Estadual':
                        cliente.inscricao_estadual = numero
                    elif descricao == 'Nire ':
                        cliente.nire = numero

                    cliente.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully updated {cnpj_cpf}'))
                except Cliente.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Cliente with CNPJ/CPF {cnpj_cpf} does not exist'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error updating {cnpj_cpf}: {e}'))

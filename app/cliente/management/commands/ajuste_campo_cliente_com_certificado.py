import csv
from django.core.management.base import BaseCommand
from cliente.models import Cliente, ClienteTipoSenha, TipoSenha
from django.db.models import Max
from django.db import models

class Command(BaseCommand):
    help = 'Update cliente field in CSV file with database IDs'

    def handle(self, *args, **kwargs):
        input_file = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/bv-clientes-certificados.csv'
        output_file = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/Updated_bv-clientes-certificados.csv'

        with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            """_summary_
            Query will be done to get the ID of the client and update the CSV file with the ID of the client.
            First: The client is searched in the database by the document.
                If not found,
                    then another search is made by the name.
            If neither is found, then a warning message is displayed.
            Else
                The client ID is updated in the CSV file.
            """

            for row in reader:


                # get the document from the row
                documento = row['DOCUMENTO']

                # First search by document to see if client already exists
                try:
                    cliente = Cliente.objects.filter(documento=documento).first()
                    if cliente:
                        row['cliente'] = cliente.id
                    else:
                        cliente_id = Cliente.objects.all().aggregate(models.Max("id"))["id__max"] + 1
                        cliente = Cliente.objects.create(id=cliente_id,documento=documento, nomerazao=row['nomerazao'])
                        cliente.save()
                        row['cliente'] = cliente.id

                    # pega TipoSenha onde descricao="Senha Certificado Digital"
                    tipo_senha = TipoSenha.objects.filter(descricao="Senha Certificado Digital").first()
                    if tipo_senha:
                        cliente_tipo_senha = ClienteTipoSenha.objects.filter(cliente=cliente, tipo_senha=tipo_senha).first()
                        if not cliente_tipo_senha:
                            cliente_tipo_senha = ClienteTipoSenha.objects.create(cliente=cliente, tipo_senha=tipo_senha, senha=row['SENHACERTIFICADO'])
                            cliente_tipo_senha.save()
                        else:
                            cliente_tipo_senha.senha = row['SENHACERTIFICADO']
                            cliente_tipo_senha.save()

                    # atualiza o campo vencimentocertificado na tabela cliente
                    cliente = Cliente.objects.get(id=cliente.id)
                    if cliente:
                        cliente.vencimentocertificado = row['VENCIMENTOCERTIFICADO'] if row['VENCIMENTOCERTIFICADO'] != "" else "2024-01-01"
                        cliente.save()

                except Cliente.DoesNotExist:
                    pass


                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS('CSV file has been updated successfully.'))

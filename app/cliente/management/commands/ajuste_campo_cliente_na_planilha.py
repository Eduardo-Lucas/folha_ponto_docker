import csv
from django.core.management.base import BaseCommand
from cliente.models import Cliente, ClienteTipoSenha
from django.db.models import Max

class Command(BaseCommand):
    help = 'Update cliente field in CSV file with database IDs'

    def handle(self, *args, **kwargs):
        input_file = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/Cliente tipo senha-2024-10-17.csv'
        output_file = '/home/edu/Projetos/folha_ponto_docker/app/cliente/management/commands/Updated_Cliente tipo senha-2024-10-17.csv'

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
            # Take the max id of ClienteTipoSenha
            max_id = ClienteTipoSenha.objects.all().aggregate(max_id=Max('id'))['max_id']
            if max_id is None:
                max_id = 1

            for row in reader:
                # update column id in the CSV file
                max_id += 1
                row['id'] = max_id

                # get the document from the row
                documento = row['CNPJ']

                # if documento[0] == '0': remove it
                if documento[0] == '0':
                    documento = documento[1:]

                # this field is going to be used to search the client in the database, in case the document is not found
                nomerazao = row['nomerazao']

                # First search by document
                try:
                    cliente = Cliente.objects.filter(documento=documento).first()
                    row['cliente'] = cliente.id
                except Cliente.DoesNotExist:
                    pass

                # If not found, search by nomerazao
                if not cliente:
                    try:
                        cliente = Cliente.objects.filter(nomerazao=nomerazao).first()
                        row['cliente'] = cliente.id
                    except Cliente.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Cliente with Documento: {documento} not found.'))

                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS('CSV file has been updated successfully.'))

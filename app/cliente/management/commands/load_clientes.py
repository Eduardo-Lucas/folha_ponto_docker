import csv

from cliente.models import Cliente
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Load Cliente from a CSV file."""

    help = "Loads Cliente."

    def handle(self, *args, **options):
        load_data_from_csv()


def load_data_from_csv():
    """Load data from csv file."""
    with open("Cliente-current.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:

            obj = Cliente(
                id=row["id"],
                tipodocumento=row["tipodocumento"],
                documento=row["documento"] if row["documento"] else 0,
                nomerazao=row["nomerazao"],
                apelidofantazia=row["apelidofantazia"],
                tipocertificado=row["tipocertificado"] if row["tipocertificado"] else 0,
                senhacertificado=row["senhacertificado"],
                vencimentocertificado=(
                    row["vencimentocertificado"]
                    if row["vencimentocertificado"]
                    else None
                ),
                logositebv=row["logositebv"],
                iniciobv=row["iniciobv"] if row["iniciobv"] else None,
                observacao=row["observacao"],
                codigosistema=row["codigosistema"] if row["codigosistema"] else None,
                situacaoentidade=row["situacaoentidade"],
                codigoterceiro=row["codigoterceiro"],
                controlarvencimentocertificado=row["controlarvencimentocertificado"],
                emiteboleto=row["emiteboleto"],
                diavencimentoboleto=(
                    row["diavencimentoboleto"] if row["diavencimentoboleto"] else 0
                ),
                grupoeconomico_id=(
                    row["grupoeconomico_id"] if row["grupoeconomico_id"] else None
                ),
                contato_id=row["contato_id"] if row["contato_id"] else None,
            )
            obj.save()
        print("Clientes have been successfully uploaded.")

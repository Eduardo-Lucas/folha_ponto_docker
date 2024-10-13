from django.core.management.base import BaseCommand
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Adjust tipo_documento based on the length of documento'

    def handle(self, *args, **kwargs):
        clientes = Cliente.objects.filter(documento__isnull=False)
        for cliente in clientes:
            if len(str(cliente.documento)) <= 11:
                cliente.tipodocumento = 1
            else:
                cliente.tipodocumento = 2
            cliente.save()
        self.stdout.write(self.style.SUCCESS('Successfully adjusted tipo_documento for all relevant records'))

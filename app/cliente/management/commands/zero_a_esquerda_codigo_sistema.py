from django.core.management.base import BaseCommand
from cliente.models import Cliente

class Command(BaseCommand):
    help = 'Fill codigosistema with zeros to the left if its length is less than 4'

    def handle(self, *args, **kwargs):
        clientes = Cliente.objects.filter(codigosistema__isnull=False)
        for cliente in clientes:
            if len(cliente.codigosistema) < 4:
                cliente.codigosistema = cliente.codigosistema.zfill(4)
                cliente.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated codigosistema for all relevant clientes'))

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from cliente.models import Cliente


class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente


class ClientAdmin(ImportExportModelAdmin):
    resource_classes = [ClienteResource]


admin.site.register(Cliente, ClientAdmin)

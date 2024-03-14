"""Admin definition for Cliente."""

from cliente.models import Cliente
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ClienteResource(resources.ModelResource):
    """Resource definition for Cliente."""

    class Meta:
        """Meta definition for ClienteResource."""

        model = Cliente


class ClientAdmin(ImportExportModelAdmin):
    """Admin definition for Cliente."""

    resource_classes = [ClienteResource]
    search_fields = ["nomerazao"]


admin.site.register(Cliente, ClientAdmin)

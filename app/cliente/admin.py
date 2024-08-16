"""Admin definition for Cliente."""

from cliente.models import Cliente, TipoSenha
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


class TipoSenhaResource(resources.ModelResource):
    """Resource definition for TipoSenha."""

    class Meta:
        """Meta definition for TipoSenhaResource."""

        model = TipoSenha


class TipoSenhaAdmin(ImportExportModelAdmin):
    """Admin definition for TipoSenha."""

    resource_classes = [TipoSenhaResource]
    search_fields = ["descricao"]

admin.site.register(Cliente, ClientAdmin)
admin.site.register(TipoSenha, TipoSenhaAdmin)

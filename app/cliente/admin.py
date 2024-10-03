"""Admin definition for Cliente."""

from cliente.models import Cliente, TipoSenha, ClienteTipoSenha
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

class ClienteTipoSenhaResource(resources.ModelResource):
    """Resource definition for ClienteTipoSenha."""

    class Meta:
        """Meta definition for ClienteTipoSenhaResource."""

        model = ClienteTipoSenha

class ClienteTipoSenhaAdmin(ImportExportModelAdmin):
    """Admin definition for ClienteTipoSenha."""

    resource_classes = [ClienteTipoSenhaResource]
    search_fields = ["cliente__nomerazao", "tipo_senha__descricao"]

admin.site.register(Cliente, ClientAdmin)
admin.site.register(TipoSenha, TipoSenhaAdmin)
admin.site.register(ClienteTipoSenha, ClienteTipoSenhaAdmin)

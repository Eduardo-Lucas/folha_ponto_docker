from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from apontamento.models import Ponto, TipoReceita



class PontoResource(resources.ModelResource):
    """Resource class for Ponto."""
    class Meta:
        """Meta class for PontoResource."""
        model = Ponto


class PontoAdmin(ImportExportModelAdmin):
    """Admin class for Ponto."""
    resource_classes = [PontoResource]
    fieldsets = (
        (
            "general", {
                "fields": ("entrada", "saida", "usuario")
            }
        ),
    )
    search_fields = ["usuario__username"]

class TipoReceitaResource(resources.ModelResource):
    """Resource class for TipoReceita."""

    class Meta:
        """Meta class for TipoReceitaResource."""
        model = TipoReceita

class TipoReceitaAdmin(ImportExportModelAdmin):
    """Admin class for TipoReceita."""
    resource_classes = [TipoReceitaResource]


admin.site.register(Ponto, PontoAdmin)
admin.site.register(TipoReceita, TipoReceitaAdmin)

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
    class Meta:
        model = TipoReceita


@admin.register(TipoReceita)
class TipoReceitaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [TipoReceitaResource]
    list_display = (
        "id",
        "descricao",
        "recibo",
        "status",
        "registra_ponto",
    )


# class TipoReceitaResource(resources.ModelResource):
#     """Resource class for TipoReceita."""

#     class Meta:
#         """Meta class for TipoReceitaResource."""
#         model = TipoReceita

# class TipoReceitaAdmin(ImportExportModelAdmin):
#     """Admin class for TipoReceita."""
#     resource_classes = [TipoReceitaResource]


admin.site.register(Ponto, PontoAdmin)
# admin.site.register(TipoReceita, TipoReceitaAdmin)

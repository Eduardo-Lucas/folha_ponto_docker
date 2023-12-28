from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from apontamento.models import Ponto, TipoReceita


class PontoResource(resources.ModelResource):
    class Meta:
        model = Ponto


class PontoAdmin(ImportExportModelAdmin):
    resource_classes = [PontoResource]
    fieldsets = (
        ("general", {"fields": ("entrada", "saida", "usuario_id")}),
    )

class TipoReceitaResource(resources.ModelResource):

    class Meta:
        model = TipoReceita

class TipoReceitaAdmin(ImportExportModelAdmin):
    resource_classes = [TipoReceitaResource]


admin.site.register(Ponto, PontoAdmin)
admin.site.register(TipoReceita, TipoReceitaAdmin)

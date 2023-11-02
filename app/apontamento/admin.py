from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from apontamento.models import Ponto


class PontoResource(resources.ModelResource):
    class Meta:
        model = Ponto


class PontoAdmin(ImportExportModelAdmin):
    resource_classes = [PontoResource]


admin.site.register(Ponto, PontoAdmin)

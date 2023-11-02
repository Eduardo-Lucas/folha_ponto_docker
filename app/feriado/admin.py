from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from feriado.models import Feriado


class FeriadoResource(resources.ModelResource):
    class Meta:
        model = Feriado


class FeriadoAdmin(ImportExportModelAdmin):
    resource_classes = [FeriadoResource]


admin.site.register(Feriado, FeriadoAdmin)

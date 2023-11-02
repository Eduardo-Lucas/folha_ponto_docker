from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from contato.models import Contato


class ContatoResource(resources.ModelResource):
    class Meta:
        model = Contato


class ContatoAdmin(ImportExportModelAdmin):
    resource_classes = [ContatoResource]


admin.site.register(Contato, ContatoAdmin)

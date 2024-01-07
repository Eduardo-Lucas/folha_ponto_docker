from contato.models import Contato
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# class ContatoResource(resources.ModelResource):
#     class Meta:
#         model = Contato


# class ContatoAdmin(ImportExportModelAdmin):
#     resource_classes = [ContatoResource]


# admin.site.register(Contato, ContatoAdmin)

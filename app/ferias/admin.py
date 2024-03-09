from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Ferias


class FeriasResource(resources.ModelResource):
    """FeriasResource."""

    class Meta:
        """Meta."""

        model = Ferias


class FeriasAdmin(ImportExportModelAdmin):
    """FeriasAdmin."""

    resource_classes = [FeriasResource]


admin.site.register(Ferias, FeriasAdmin)

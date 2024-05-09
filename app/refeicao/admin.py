from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Refeicao


class RefeicaoResource(resources.ModelResource):
    """FeriasResource."""

    class Meta:
        """Meta."""

        model = Refeicao


class RefeicaoAdmin(ImportExportModelAdmin):
    """FeriasAdmin."""

    resource_classes = [RefeicaoResource]


admin.site.register(Refeicao, RefeicaoAdmin)

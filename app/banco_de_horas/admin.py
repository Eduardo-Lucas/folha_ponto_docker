from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import BancoDeHoras


class BancoDeHorasResource(resources.ModelResource):
    """Resource class for BancoDeHoras."""

    class Meta:
        """Meta class for BancoDeHorasResource."""

        model = BancoDeHoras


class BancoDeHorasAdmin(ImportExportModelAdmin):
    """Admin class for BancoDeHoras."""

    resource_classes = [BancoDeHorasResource]
    fieldsets = (
        (
            "general",
            {
                "fields": (
                    "user",
                    "periodo_apurado",
                    "saldo_anterior",
                    "total_credor",
                    "total_devedor",
                    "compensacao",
                    "pagamento",
                )
            },
        ),
    )
    search_fields = ["user__username"]


admin.site.register(BancoDeHoras, BancoDeHorasAdmin)

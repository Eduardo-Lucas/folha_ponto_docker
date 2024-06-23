"""
Module docstring describing the purpose of this module.
"""

from django.contrib import admin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Departamento, UserProfile

class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [UserProfileResource]
    list_display = (
        "user",
        "nome",
        "tipo_receita",
        "cargahoraria",
        "bateponto",
        "semintervaloalmoco",
        "almoco",
    )


#admin.site.register(UserProfile, UserProfileAdmin)


class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = Departamento


class DepartamentoAdmin(ImportExportModelAdmin):
    resource_classes = [DepartamentoResource]


admin.site.register(Departamento, DepartamentoAdmin)


# add menu item to come back to home page from admin page
admin.site.site_url = "/"

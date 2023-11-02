from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.models import User
from .models import UserProfile


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


class UserProfileAdmin(ImportExportModelAdmin):
    resource_classes = [UserProfileResource]


admin.site.register(UserProfile, UserProfileAdmin)

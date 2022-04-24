from django.contrib import admin
from django.db import models
from django.forms import Textarea
from import_export import resources
from import_export.admin import ImportExportMixin

from reestr.models import Service


class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        import_id_fields = ['service_code']


@admin.register(Service)
class ServiceAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ServiceResource
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 5,
                   'cols': 100})},
    }

    list_display = ('service_code', 'name',)
    list_display_links = ('service_code', 'name',)
    search_fields = ('service_code', 'name',)

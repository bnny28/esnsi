from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput
from import_export import resources
from import_export.admin import ImportExportMixin

from reestr.models import Organization


class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization
        import_id_fields = ['code']


@admin.register(Organization)
class OrganizationAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrganizationResource

    # def publish_this(self, request, obj):
    #     pass
    #
    # publish_this.label = "Мое действие в форме"  # optional
    # publish_this.short_description = "Пример комментария моего действия в форме"  # optional
    #
    # change_actions = ('publish_this',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 100})},
        models.CharField: {'widget': TextInput(attrs={'size': '98'})},
    }

    list_display = ('code', 'short_title', 'inn', 'title',)
    list_display_links = ('code', 'short_title',)
    search_fields = ('title', 'code', 'inn',)


admin.site.site_title = 'Данные для ЕСНСИ Калужская обл.'
admin.site.site_header = 'Данные для ЕСНСИ Калужская область'

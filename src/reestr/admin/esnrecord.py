from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.widgets import ForeignKeyWidget

from reestr.models import Service, EsnRecord, Department


class EsnRecordResource(resources.ModelResource):
    organization = fields.Field(column_name='CODE')
    service = fields.Field(column_name='SERVICE_CODE', attribute='service',
                           widget=ForeignKeyWidget(Service, 'service_code'))
    title = fields.Field(column_name='TITLE')
    short_title = fields.Field(column_name='SHORT_TITLE')
    address = fields.Field(column_name='ADDRESS', attribute='department',
                           widget=ForeignKeyWidget(Department, 'address'))
    phone = fields.Field(column_name='PHONE', attribute='department',
                         widget=ForeignKeyWidget(Department, 'format_phones'))
    email = fields.Field(column_name='EMAIL', attribute='department',
                         widget=ForeignKeyWidget(Department, 'email'))
    regokato = fields.Field(column_name='REGOKATO')
    inn = fields.Field(column_name='INN')
    type_organization = fields.Field(column_name='TYPE_SERVICE_CODE', attribute='department',
                                     widget=ForeignKeyWidget(Department, 'services_type'))

    @staticmethod
    def dehydrate_regokato(esnrecord):
        return '29000000000'

    @staticmethod
    def dehydrate_organization(esnrecord):
        return str(esnrecord.department.organization.code)

    @staticmethod
    def dehydrate_service(esnrecord):
        return str(esnrecord.service.service_code)

    @staticmethod
    def dehydrate_inn(esnrecord):
        return str(esnrecord.department.organization.inn)

    @staticmethod
    def dehydrate_title(esnrecord):
        return str(esnrecord.department.organization.title)

    @staticmethod
    def dehydrate_short_title(esnrecord):
        return str(esnrecord.department.organization.short_title)

    class Meta:
        model = EsnRecord
        exclude = ('id', 'department',)


@admin.register(EsnRecord)
class EsnRecordAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EsnRecordResource
    list_display = ('org_code', 'service_code', 'org_short_title', 'dep_address', 'dep_phones', 'dep_email',)
    list_display_links = ('service_code',)
    autocomplete_fields = ['service', 'department', ]

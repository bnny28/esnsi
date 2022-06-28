from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_object_actions import DjangoObjectActions
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
    kpp = fields.Field(column_name='KPP')
    oktmo = fields.Field(column_name='OKTMO')
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
    def dehydrate_kpp(esnrecord):
        return str(esnrecord.department.organization.kpp) if esnrecord.department.organization.kpp else ''

    @staticmethod
    def dehydrate_oktmo(esnrecord):
        return str(esnrecord.department.organization.oktmo) if esnrecord.department.organization.oktmo else ''

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
class EsnRecordAdmin(DjangoObjectActions, ExportMixin, admin.ModelAdmin):
    resource_class = EsnRecordResource

    def del_all(self, request, queryset):
        EsnRecord.objects.all().delete()

    del_all.label = "Удалить все записи ЕСНСИ"  # optional

    def redirect_to_export(self, request, obj):
        return HttpResponseRedirect(reverse('admin:%s_%s_export' % self.get_model_info()))

    redirect_to_export.label = "Экспорт"

    changelist_actions = ('del_all', 'redirect_to_export')

    search_fields = ('department__phones', 'department__address', 'department__organization__title',
                     'department__organization__code', 'service__service_code',
                     'department__organization__short_title',)
    list_display = ('org_code', 'service_code', 'org_short_title', 'dep_address', 'dep_phones', 'dep_email',)
    list_display_links = ('service_code',)
    autocomplete_fields = ['service', 'department', ]

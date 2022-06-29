import re

from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_object_actions import DjangoObjectActions
from import_export import resources
from import_export.admin import ImportExportMixin

from reestr.models import EsnRecord, Department, Service


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department


@admin.register(Department)
class DepartmentAdmin(DjangoObjectActions, ImportExportMixin, admin.ModelAdmin):
    resource_class = DepartmentResource

    # def publish_this(self, request, obj):
    #     pass
    #
    # publish_this.label = "Мое действие в форме"  # optional
    # publish_this.short_description = "Пример комментария моего действия в форме"  # optional
    #
    # change_actions = ('publish_this',)

    def make_esnsi_records(self, request, queryset):
        EsnRecord.objects.all().delete()
        bulk_list = list()
        for dep in queryset.prefetch_related("services").all():
            services = dep.services.all()
            for service in services:
                bulk_list.append(EsnRecord(department=dep, service=service))
        EsnRecord.objects.bulk_create(bulk_list)
        return HttpResponseRedirect(
            reverse('admin:%s_%s_changelist' % (self.model._meta.app_label, 'esnrecord')))

    make_esnsi_records.label = "Сформировать записи ЕСНСИ"  # optional

    def redirect_to_export(self, request, obj):
        return HttpResponseRedirect(reverse('admin:%s_%s_export' % self.get_model_info()))

    redirect_to_export.label = "Экспорт"

    def redirect_to_import(self, request, obj):
        return HttpResponseRedirect(reverse('admin:%s_%s_import' % self.get_model_info()))

    redirect_to_import.label = "Импорт"

    changelist_actions = ('make_esnsi_records', 'redirect_to_import', 'redirect_to_export')

    @admin.action(description='Объединить')
    def make_join(self, request, queryset):
        dep = queryset.first()
        services_list = list()
        for obj in queryset:
            services_list.extend(list(obj.services.values_list('service_code', flat=True)))
        services = Service.objects.filter(service_code__in=services_list)
        if len(services) > 0:
            dep.services.set(services)
            dep.save()
        dep = queryset.first()
        for obj in queryset:
            if obj is not dep:
                obj.delete()

    @admin.action(description='Адрес сделать одинаковым')
    def make_adr(self, request, queryset):
        dep = queryset.first()
        queryset.update(address=dep.address)

    @admin.action(description='Email сделать одинаковым')
    def make_email(self, request, queryset):
        dep = queryset.first()
        queryset.update(email=dep.email)

    @admin.action(description='Телефон преобразовать')
    def make_phones(self, request, queryset):
        for obj in queryset:
            obj.phones = ''.join(re.findall(r"\d|,|;", obj.phones))
            obj.save()

    @admin.action(description='Создать на основе')
    def make_phones(self, request, queryset):
        sample = queryset.first()
        dep = Department(
            organization=sample.organization,
            address=sample.address,
            phones=sample.phones,
            email=sample.email)
        dep.save()
        return HttpResponseRedirect(
            reverse("admin:%s_%s_change" % (self.model._meta.app_label, self.model._meta.model_name), args=(dep.id,)))

    def get_queryset(self, request):
        qs = super(DepartmentAdmin, self).get_queryset(request)
        return qs.prefetch_related('services')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 60})},
        models.CharField: {'widget': TextInput(attrs={'size': '60'})},
    }

    actions = [make_phones]
    list_display = ('org_short_title', 'service_codes', 'address',)
    list_display_links = ('org_short_title', 'service_codes',)
    search_fields = ('phones', 'address', 'organization__short_title', 'organization__title', 'organization__code',
                     'services__service_code')
    # list_editable = ('address',)
    list_filter = ('services__service_code',)
    filter_horizontal = ('services',)
    autocomplete_fields = ['organization', ]

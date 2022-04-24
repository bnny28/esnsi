import re

from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django_object_actions import DjangoObjectActions

from reestr.models import ImpRecord, Organization, Service, Department


@admin.register(ImpRecord)
class ImpRecordAdmin(DjangoObjectActions, admin.ModelAdmin):

    def make_records(self, request, queryset):
        codes = queryset.values('code').distinct()
        for item in codes:
            children = queryset.filter(code=item['code']).first()
            title = children.title.strip().lower()
            short_title = children.short_title.strip().lower()
            inn = str(children.inn).strip().lower()
            children = queryset.filter(code=item['code'])
            is_equal = True
            for itm in children:
                if title != itm.title.strip().lower():
                    print('Не совпадает title')
                    is_equal = False
                    break
                elif short_title != itm.short_title.strip().lower():
                    print('Не совпадает short_title')
                    is_equal = False
                    break
                elif inn != str(itm.inn).strip().lower():
                    print('Не совпадает inn')
                    is_equal = False
                    break
            if is_equal:
                children = queryset.filter(code=item['code']).first()
                org = Organization.objects.create(
                    code=item['code'],
                    title=children.title.strip(),
                    short_title=children.short_title.strip(),
                    inn=children.inn)
                org.save()
                children = queryset.filter(code=item['code'])
                for itm in children:
                    dep = Department.objects.create(
                        organization=org,
                        address=itm.address.strip().replace(r'(. )', '.'),
                        phones=''.join(re.findall(r"\d|,|;", itm.phone.strip())),
                        email=itm.email.strip(),
                        services_type=itm.type_service_code.strip() if itm.type_service_code else ''
                    )
                    dep.save()
                    services = Service.objects.filter(service_code__in=[itm.service_code])
                    if len(services) > 0:
                        dep.services.set(services)
                    else:
                        dep.note = str(itm.service_code) + ' - отсутствующий код услуги'
                    dep.save()
                ImpRecord.objects.filter(code=item['code']).delete()
            else:
                print('Не совпадает ' + str(item['code']))
            break

        # EsnRecord.objects.all().delete()
        # bulk_list = list()
        # for org in queryset.prefetch_related("services").all():
        #     services = org.services.all()
        #     for service in services:
        #         bulk_list.append(EsnRecord(organization=org, service=service))
        # EsnRecord.objects.bulk_create(bulk_list)
        pass

    make_records.label = "Сформировать записи"  # optional

    changelist_actions = ('make_records',)

    @admin.action(description='Title, Short_title, INN -  сделать одинаковыми')
    def prepare_org(self, request, queryset):
        org = queryset.first()
        queryset.update(title=org.title)
        queryset.update(short_title=org.short_title)
        queryset.update(inn=org.inn)

    @admin.action(description='Сельского поселения -> СП')
    def make_sp(self, request, queryset):
        for obj in queryset:
            obj.short_title = obj.short_title.replace('сельского поселения', 'СП')
            obj.save()

    @admin.action(description='Capitalize')
    def capitalize(self, request, queryset):
        for obj in queryset:
            obj.title = obj.title.capitalize()
            obj.save()

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 2,
                   'cols': 100})},
    }

    actions = [prepare_org, make_sp, capitalize]
    list_display = ('code', 'title', 'short_title', 'inn',)
    list_display_links = ('code',)
    list_editable = ('title', 'short_title', 'inn',)
    list_filter = ('code',)

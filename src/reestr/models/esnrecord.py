from django.core.exceptions import ValidationError
from django.db import models
from django_admin_display import admin_display


class EsnRecord(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, verbose_name='Услуга')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name='Подразделение')

    @property
    @admin_display(short_description="Организация", )
    def org_code(self):
        return self.department.organization.code

    @property
    @admin_display(short_description="Услуга", )
    def service_code(self):
        return self.service.service_code

    @property
    @admin_display(short_description="Наименование организации", )
    def org_short_title(self):
        return self.department.organization.short_title

    @property
    @admin_display(short_description="Адрес подразделения", )
    def dep_address(self):
        return self.department.address

    @property
    @admin_display(short_description="Телефон", )
    def dep_phones(self):
        return self.department.format_phones

    @property
    @admin_display(short_description="Email", )
    def dep_email(self):
        return self.department.email

    def validate_unique(self, *args, **kwargs):
        qs = EsnRecord.objects.filter(service=self.service)
        if qs.filter(department__organization=self.department.organization).exists():
            raise ValidationError({'service': ['Код услуги должен быть уникальным для организации', ]})
        super(EsnRecord, self).validate_unique(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(EsnRecord, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.department.organization)

    class Meta:
        verbose_name = 'Запись ЕСНСИ'
        verbose_name_plural = 'Записи ЕСНСИ'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['service', 'organization'],
        #         name='compose_key'
        #     )
        # ]

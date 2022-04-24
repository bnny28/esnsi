from django.db import models


class ImpRecord(models.Model):
    code = models.PositiveBigIntegerField(verbose_name='CODE*')
    service_code = models.BigIntegerField(verbose_name='SERVICE_CODE*')
    title = models.TextField(max_length=500, verbose_name='TITLE*')
    short_title = models.TextField(max_length=500, verbose_name='SHORT_TITLE*')
    address = models.TextField(max_length=500, verbose_name='ADDRESS*')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='PHONE')
    email = models.EmailField(verbose_name='EMAIL*')
    inn = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='INN*')
    type_service_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='TYPE_SERVICE_CODE')

    class Meta:
        verbose_name = 'Запись для импорта'
        verbose_name_plural = 'Записи для импорта'
        ordering = ['code']

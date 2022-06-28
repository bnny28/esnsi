from django.db import models
from django.core.exceptions import ValidationError


class Service(models.Model):
    service_code = models.BigIntegerField(primary_key=True, verbose_name='Код услуги*')
    name = models.TextField(max_length=600, verbose_name='Наименование услуги*')
    responsible = models.TextField(max_length=500, blank=True, null=True,
                                   verbose_name='Орган, ответственный за оказание услуги')
    url = models.URLField(blank=True, null=True, verbose_name='URL адрес предоставления на ЕПГУ')
    note = models.TextField(max_length=500, blank=True, null=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания', null=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['-service_code']

    def clean(self):
        if len(str(self.service_code)) > 13:
            raise ValidationError(
                {'service_code': "Код услуги должен быть не более 13 знаков"})

    def __str__(self):
        return '%s - %s' % (self.service_code, self.name)

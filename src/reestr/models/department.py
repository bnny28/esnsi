import re

from django.core.exceptions import ValidationError
from django.db import models
from django_admin_display import admin_display

TYPE_CHOICES = (
    ("municipal", "Муниципальная"),
    ("regional", "Региональная"),
)


class Department(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, verbose_name='Организация*')
    address = models.TextField(max_length=500, verbose_name='Адрес*',
                               help_text='пример: 249913 Калужская область, Юхновский район, д.Рыляки, ул.Мира, д.1')
    phones = models.CharField(max_length=50, verbose_name='Телефоны*',
                              help_text='пример: 84843155555,66666 Начиная с цифры 8 '
                                        'и кодом города, всего 11 цифр. Через запятую, без пробелов')
    email = models.EmailField(verbose_name='Электронная почта*')
    services = models.ManyToManyField('Service', verbose_name='Услуги*')
    services_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=True, null=True,
                                     verbose_name='Тип услуги',
                                     help_text='Необходимо указать при предоставления некоторых услуг:'
                                               ' -10000115350, -10000115362, -10000115364 Эти услуги только'
                                               ' в !ОТДЕЛЬНОМ ПОДРАЗДЕЛЕНИИ')
    note = models.TextField(max_length=500, blank=True, null=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def clean(self):
        self.address = self.address.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
        match = re.fullmatch(r'(|\d{11}|\d{11}((,)\d{5,11})+)', self.phones)
        if not match:
            raise ValidationError(
                {'phones': "Телефоны не соответствуют формату (пример: 84843155555,89102222222)"})

    @property
    @admin_display(
        short_description="Телефоны",
    )
    def format_phones(self):
        new_pones = list()
        if self.phones is not None and len(self.phones.strip()) != 0:
            phones = self.phones.split(',')
            for item in phones:
                p = item.strip()
                if len(p) < 11:
                    new_pones.append(p[:-4] + '-' + p[-4:-2] + '-' + p[-2:])
                elif p[:2] == '89' or p[:4] == '8800':
                    new_pones.append(p[0] + '(' + p[1:4] + ')' + p[4:7] + '-' + p[7:9] + '-' + p[-2:])
                elif p[1:5] == '4842':
                    new_pones.append(p[0] + '(' + p[1:5] + ')' + p[5:7] + '-' + p[7:9] + '-' + p[-2:])
                else:
                    new_pones.append(p[0] + '(' + p[1:6] + ')' + p[6:7] + '-' + p[7:9] + '-' + p[-2:])
            return ', '.join([p for p in new_pones])
        return ''

    @property
    @admin_display(
        short_description="Коды услуг",
    )
    def service_codes(self):
        srv = self.services.all()
        return (",\t".join([str(p.service_code) for p in srv])) + ' \t~' + str(len(srv))

    @property
    @admin_display(
        short_description="Организация",
    )
    def org_short_title(self):
        return self.organization.short_title

    def __str__(self):
        return '%s - %s' % (self.organization.code, self.organization.short_title)

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['organization', 'address']


# @receiver(post_save, sender=Department, dispatch_uid="update_stock_count")
# def update_stock(sender, instance, **kwargs):
#     time.sleep(3)
#     print(len(instance.services.values()))

from django.core.exceptions import ValidationError
from django.db import models

TYPE_CHOICES = (
    ("municipal", "Муниципальная"),
    ("regional", "Региональная"),
)


class Organization(models.Model):
    code = models.PositiveBigIntegerField(primary_key=True, verbose_name='ОГРН*')
    title = models.TextField(max_length=500, unique=True, verbose_name='Полное наименование*')
    short_title = models.TextField(max_length=500, unique=True, verbose_name='Краткое наименование*')
    inn = models.PositiveBigIntegerField(unique=True, verbose_name='ИНН*')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def clean(self):
        self.title = self.title.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
        self.short_title = self.short_title.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
        if len(str(self.code)) != 13:
            raise ValidationError(
                {'code': "ОГРН должен быть 13 цифр ровно"})
        if len(str(self.inn)) != 10:
            raise ValidationError(
                {'inn': "ИНН должен быть 10 цифр ровно"})

    #
    # @property
    # @admin_display(
    #     short_description="Адрес",
    # )
    # def format_address(self):
    #     if self.address is not None and len(self.address.strip()) != 0:
    #         return self.address.strip()
    #     else:
    #         if self.post_index is not None and len(str(self.post_index)) != 0:
    #             add = str(self.post_index) + ' Калужская область'
    #         else:
    #             add = 'Калужская область'
    #         if self.region is not None and len(self.region.strip()) != 0:
    #             add += ', ' + self.region.strip()
    #         if self.city is not None and len(self.city.strip()) != 0:
    #             add += ', ' + self.city.strip()
    #         if self.place is not None and len(self.place.strip()) != 0:
    #             add += ', ' + self.place.strip()
    #         if self.building is not None and len(self.building.strip()) != 0:
    #             add += ', ' + self.building.strip()
    #         return add

    def __str__(self):
        # return str(self.code)
        return '%s - %s' % (self.code, self.short_title)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['code']

# Generated by Django 3.2.13 on 2022-04-24 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(help_text='пример: 249913 Калужская область, Юхновский район, д.Рыляки, ул.Мира, д.1', max_length=500, verbose_name='Адрес*')),
                ('phones', models.CharField(help_text='пример: 84843155555,66666 C 8 вначале и кодом города 11 цифр. Через запятую, без пробелов', max_length=50, verbose_name='Телефоны*')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта*')),
                ('services_type', models.CharField(blank=True, choices=[('municipal', 'Муниципальная'), ('regional', 'Региональная')], help_text='Необходимо указать при предоставления некоторых услуг: -10000115350, -10000115362, -10000115364 Эти услуги только в !ОТДЕЛЬНОМ ПОДРАЗДЕЛЕНИИ', max_length=10, null=True, verbose_name='Тип услуги')),
                ('note', models.TextField(blank=True, max_length=500, null=True, verbose_name='Примечания')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ImpRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveBigIntegerField(verbose_name='CODE*')),
                ('service_code', models.BigIntegerField(verbose_name='SERVICE_CODE*')),
                ('title', models.TextField(max_length=500, verbose_name='TITLE*')),
                ('short_title', models.TextField(max_length=500, verbose_name='SHORT_TITLE*')),
                ('address', models.TextField(max_length=500, verbose_name='ADDRESS*')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='PHONE')),
                ('email', models.EmailField(max_length=254, verbose_name='EMAIL*')),
                ('inn', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='INN*')),
                ('type_service_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='TYPE_SERVICE_CODE')),
            ],
            options={
                'verbose_name': 'Запись для импорта',
                'verbose_name_plural': 'Записи для импорта',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('code', models.PositiveBigIntegerField(primary_key=True, serialize=False, verbose_name='ОГРН*')),
                ('title', models.TextField(max_length=500, unique=True, verbose_name='Полное наименование*')),
                ('short_title', models.TextField(max_length=500, unique=True, verbose_name='Краткое наименование*')),
                ('inn', models.PositiveBigIntegerField(unique=True, verbose_name='ИНН*')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_code', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Код услуги*')),
                ('name', models.TextField(max_length=600, verbose_name='Наименование услуги*')),
                ('responsible', models.TextField(blank=True, max_length=500, null=True, verbose_name='Орган, ответственный за оказание услуги')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL адрес предоставления на ЕПГУ')),
                ('note', models.TextField(blank=True, max_length=500, null=True, verbose_name='Примечания')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['-service_code'],
            },
        ),
        migrations.CreateModel(
            name='EsnRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reestr.department', verbose_name='Подразделение')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reestr.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Запись ЕСНСИ',
                'verbose_name_plural': 'Записи ЕСНСИ',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reestr.organization', verbose_name='Организация*'),
        ),
        migrations.AddField(
            model_name='department',
            name='services',
            field=models.ManyToManyField(to='reestr.Service', verbose_name='Услуги*'),
        ),
    ]
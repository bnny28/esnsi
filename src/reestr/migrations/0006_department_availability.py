# Generated by Django 3.2.13 on 2022-07-15 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reestr', '0005_alter_organization_kpp'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='availability',
            field=models.BooleanField(default=True),
        ),
    ]

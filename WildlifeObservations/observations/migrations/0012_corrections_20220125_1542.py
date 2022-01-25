# Generated by Django 3.2.11 on 2022-01-25 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0011_model_validation_20220125_1448'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meteorologyconditions',
            options={'verbose_name_plural': 'Meteorological conditions'},
        ),
        migrations.AlterField(
            model_name='plot',
            name='position',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
# Generated by Django 3.2.11 on 2022-01-25 10:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0005_alter_identifications_20220125_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='created_date',
            new_name='created_on',
        ),
        migrations.AddField(
            model_name='observation',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='visit',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

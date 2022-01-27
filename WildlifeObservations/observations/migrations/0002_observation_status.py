# Generated by Django 3.2.11 on 2022-01-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='status',
            field=models.CharField(blank=True, choices=[('Observed', 'Observed'), ('Specimen', 'Specimen'), ('Lost', 'Lost')], max_length=10, null=True),
        ),
    ]

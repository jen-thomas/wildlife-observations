# Generated by Django 3.2.11 on 2022-05-05 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0009_identification_subfamily'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonomygenus',
            name='subfamily',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomysubfamily'),
        ),
    ]

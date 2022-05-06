# Generated by Django 3.2.11 on 2022-05-06 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0013_alter_identification_confidence_reason'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='identification',
            constraint=models.CheckConstraint(check=models.Q(('confidence', 'Confirmed'), ('confidence_reason__in', ('Small_nymph_hard_to_ID', 'Cannot_determine_further', 'ID_certain'))), name='observations_identification_check_confirmed_confidence_reasons'),
        ),
    ]

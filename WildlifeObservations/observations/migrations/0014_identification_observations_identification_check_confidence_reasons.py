# Generated by Django 3.2.11 on 2022-05-06 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0013_alter_identification_confidence_reason'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='identification',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('confidence', 'Confirmed'), ('confidence_reason__in', ('Small_nymph_hard_to_ID', 'Cannot_determine_further', 'ID_certain'))), models.Q(('confidence__in', ('Check', 'Check_in_museum')), ('confidence_reason', 'ID_needs_confirmation')), models.Q(('confidence', 'In_progress'), ('confidence_reason', 'ID_incomplete')), models.Q(('confidence', 'Review'), ('confidence_reason', 'ID_uncertain')), models.Q(('confidence', 'Redo'), ('confidence_reason', 'ID_incorrect')), _connector='OR'), name='observations_identification_check_confidence_reasons'),
        ),
    ]
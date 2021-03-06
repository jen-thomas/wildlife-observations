# Generated by Django 3.2.11 on 2022-05-05 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0012_identification_confidence_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identification',
            name='confidence_reason',
            field=models.CharField(blank=True, choices=[('ID_certain', 'ID certain'), ('ID_uncertain', 'ID uncertain'), ('ID_incomplete', 'ID incomplete'), ('ID_needs_confirmation', 'ID needs confirmation'), ('ID_incorrect', 'ID incorrect'), ('Cannot_determine_further', 'Cannot determine further'), ('Small_nymph_hard_to_ID', 'Small nymph hard to ID')], max_length=30, null=True),
        ),
    ]

# Generated by Django 3.2.11 on 2022-05-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0014_identification_observations_identification_check_confidence_reasons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identification',
            name='confidence',
            field=models.CharField(blank=True, choices=[('In_progress', 'In progress'), ('Check', 'Check'), ('Check_in_museum', 'Check in museum'), ('Confirmed', 'Confirmed'), ('Redo', 'Redo'), ('Review', 'Review')], max_length=30, null=True),
        ),
    ]

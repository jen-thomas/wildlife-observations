# Generated by Django 3.2.11 on 2022-01-25 10:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0004_alter_identification_identification_guide'),
    ]

    operations = [
        migrations.AddField(
            model_name='identification',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='identification',
            name='date_of_identification',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='identification',
            name='confidence',
            field=models.CharField(blank=True, choices=[('In_progress', 'In progress'), ('Check', 'Check'), ('Confirmed', 'Confirmed'), ('Redo', 'Redo')], max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='identification',
            name='identification_guide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.identificationguide'),
        ),
        migrations.AlterField(
            model_name='identification',
            name='identification_notes',
            field=models.TextField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='identification',
            name='sex',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Unknown', 'Unknown')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='identification',
            name='species',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.speciesname'),
        ),
        migrations.AlterField(
            model_name='identification',
            name='stage',
            field=models.CharField(blank=True, choices=[('Adult', 'Adult'), ('Nymph', 'Nymph'), ('Unknown', 'Unknown')], max_length=7, null=True),
        ),
    ]

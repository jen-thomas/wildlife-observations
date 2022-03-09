# Generated by Django 3.2.11 on 2022-03-09 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0002_add_observation_notes_20220309_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='current_preservation',
            field=models.CharField(choices=[('Frozen', 'Frozen'), ('Alcohol', 'Alcohol'), ('Pinned', 'Pinned'), ('NA', 'NA')], default='Frozen', max_length=10),
        ),
        migrations.AddField(
            model_name='observation',
            name='original_preservation',
            field=models.CharField(choices=[('Frozen', 'Frozen'), ('Alcohol', 'Alcohol'), ('Pinned', 'Pinned'), ('NA', 'NA')], default='Frozen', max_length=10),
        ),
    ]

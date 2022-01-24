# Generated by Django 3.2.11 on 2022-01-24 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0002_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specimen_id', models.CharField(max_length=22, unique=True)),
                ('length_head_abdomen', models.FloatField()),
                ('length_head_tegmina', models.FloatField()),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.visit')),
            ],
        ),
    ]

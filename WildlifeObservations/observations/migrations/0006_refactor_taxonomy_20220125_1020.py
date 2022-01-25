# Generated by Django 3.2.11 on 2022-01-25 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0005_species_taxonomy_20220125_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxonomyFamily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Taxonomy families',
            },
        ),
        migrations.CreateModel(
            name='TaxonomySpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latin_name', models.CharField(max_length=255, unique=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyfamily')),
            ],
            options={
                'verbose_name_plural': 'Taxonomy species',
            },
        ),
        migrations.CreateModel(
            name='TaxonomySuborder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suborder', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Taxonomy sub-orders',
            },
        ),
        migrations.AlterModelOptions(
            name='speciesname',
            options={'verbose_name_plural': 'Species names'},
        ),
        migrations.AlterModelOptions(
            name='taxonomyorder',
            options={'verbose_name_plural': 'Taxonomy orders'},
        ),
        migrations.RenameModel(
            old_name='Species',
            new_name='SpeciesName',
        ),
        migrations.DeleteModel(
            name='Taxonomy',
        ),
        migrations.AddField(
            model_name='taxonomysuborder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyorder'),
        ),
        migrations.AddField(
            model_name='taxonomyfamily',
            name='suborder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomysuborder'),
        ),
        migrations.AlterField(
            model_name='speciesname',
            name='latin_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyspecies'),
        ),
    ]

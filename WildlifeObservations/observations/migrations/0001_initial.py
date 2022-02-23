# Generated by Django 3.2.11 on 2022-02-23 16:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IdentificationGuide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('author', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=30)),
                ('site_name', models.CharField(max_length=5, unique=True)),
                ('altitude_band', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('latitude_start', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude_start', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('altitude_start', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('gps_number_satellites_start', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('gps_accuracy_start', models.IntegerField(blank=True, null=True)),
                ('gps_aspect_start', models.FloatField(blank=True, null=True)),
                ('latitude_end', models.FloatField(validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude_end', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('altitude_end', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('gps_number_satellites_end', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('gps_accuracy_end', models.IntegerField(blank=True, null=True)),
                ('gps_aspect_end', models.FloatField(blank=True, null=True)),
                ('transect_length', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('transect_description', models.TextField(blank=True, default='', max_length=2048)),
                ('notes', models.TextField(blank=True, default='', max_length=2048)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Viking Topo', 'Viking Topo'), ('GPS', 'GPS'), ('DEM', 'DEM'), ('OsmAnd', 'OsmAnd')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TaxonomyClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taxclass', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Taxonomy classes',
            },
        ),
        migrations.CreateModel(
            name='TaxonomyFamily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Taxonomy families',
            },
        ),
        migrations.CreateModel(
            name='TaxonomyGenus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genus', models.CharField(max_length=255, unique=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyfamily')),
            ],
            options={
                'verbose_name_plural': 'Taxonomy genera',
            },
        ),
        migrations.CreateModel(
            name='TaxonomyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=255, unique=True)),
                ('taxclass', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyclass')),
            ],
            options={
                'verbose_name_plural': 'Taxonomy orders',
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.site')),
            ],
        ),
        migrations.CreateModel(
            name='VegetationStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage_vegetation_cover', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('percentage_bare_ground', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('percentage_rock', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('height_75percent', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('max_height', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('density_01', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('density_02', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('density_03', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('density_04', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('density_05', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('notes', models.TextField(blank=True, default='', max_length=2048)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('plot', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='observations.plot')),
            ],
        ),
        migrations.CreateModel(
            name='TaxonomySuborder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suborder', models.CharField(max_length=255, unique=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyorder')),
            ],
            options={
                'verbose_name_plural': 'Taxonomy sub-orders',
            },
        ),
        migrations.CreateModel(
            name='TaxonomySpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latin_name', models.CharField(max_length=255, unique=True)),
                ('common_name_english', models.CharField(blank=True, max_length=100, null=True)),
                ('common_name_catalan', models.CharField(blank=True, max_length=100, null=True)),
                ('common_name_spanish', models.CharField(blank=True, max_length=100, null=True)),
                ('genus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomygenus')),
            ],
            options={
                'verbose_name_plural': 'Taxonomy species',
            },
        ),
        migrations.AddField(
            model_name='taxonomyfamily',
            name='suborder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomysuborder'),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('method', models.CharField(choices=[('Net', 'Net'), ('Hand', 'Hand')], max_length=5)),
                ('repeat', models.IntegerField(choices=[(1, 'One'), (2, 'Two')])),
                ('observer', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.visit')),
            ],
        ),
        migrations.AddField(
            model_name='site',
            name='altitude_end_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='observations.source'),
        ),
        migrations.AddField(
            model_name='site',
            name='altitude_start_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='observations.source'),
        ),
        migrations.AddField(
            model_name='site',
            name='latitude_end_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='observations.source'),
        ),
        migrations.AddField(
            model_name='site',
            name='latitude_start_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='observations.source'),
        ),
        migrations.AddField(
            model_name='site',
            name='longitude_end_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='observations.source'),
        ),
        migrations.AddField(
            model_name='site',
            name='longitude_start_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='observations.source'),
        ),
        migrations.AddField(
            model_name='site',
            name='transect_length_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.source'),
        ),
        migrations.AddField(
            model_name='plot',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.visit'),
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specimen_label', models.CharField(max_length=22, unique=True, validators=[django.core.validators.RegexValidator(code='Invalid format', message='Format is sitename yyyymmdd methodrepeat specimen', regex='^[A-Z]{3}[0-9]{2} [0-9]{8} [A-Z]{1}[0-9]{1} [A-Z]{1}[0-9]{3}$')])),
                ('length_head_abdomen', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('length_head_tegmina', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('Observed', 'Observed'), ('Specimen', 'Specimen'), ('Lost', 'Lost')], max_length=10)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.survey')),
            ],
        ),
        migrations.CreateModel(
            name='MeteorologyConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloud_coverage_start', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
                ('wind_start', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('rain_start', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('cloud_coverage_end', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)])),
                ('wind_end', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('rain_end', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('notes', models.TextField(blank=True, default='', max_length=2048)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('survey', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='observations.survey')),
            ],
            options={
                'verbose_name_plural': 'Meteorological conditions',
            },
        ),
        migrations.CreateModel(
            name='Identification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification_notes', models.TextField(blank=True, max_length=2048, null=True)),
                ('sex', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Unknown', 'Unknown')], max_length=7, null=True)),
                ('stage', models.CharField(blank=True, choices=[('Adult', 'Adult'), ('Nymph', 'Nymph'), ('Unknown', 'Unknown')], max_length=7, null=True)),
                ('confidence', models.CharField(choices=[('In_progress', 'In progress'), ('Check', 'Check'), ('Confirmed', 'Confirmed'), ('Redo', 'Redo'), ('Yes', 'Yes'), ('Review', 'Review')], max_length=11)),
                ('date_of_identification', models.DateField(blank=True, null=True)),
                ('notebook', models.CharField(max_length=10)),
                ('comments', models.TextField(blank=True, max_length=1000, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyfamily')),
                ('genus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomygenus')),
                ('identification_guide', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.identificationguide')),
                ('observation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='observations.observation')),
                ('species', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomyspecies')),
                ('suborder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='observations.taxonomysuborder')),
            ],
        ),
        migrations.AddConstraint(
            model_name='visit',
            constraint=models.UniqueConstraint(fields=('site', 'date'), name='observations_visit_site_date_unique_relationships'),
        ),
        migrations.AddConstraint(
            model_name='survey',
            constraint=models.UniqueConstraint(fields=('visit', 'method', 'repeat'), name='observations_survey_visit_method_repeat_unique_relationships'),
        ),
        migrations.AddConstraint(
            model_name='survey',
            constraint=models.UniqueConstraint(fields=('visit', 'start_time'), name='observations_survey_visit_start_unique_relationships'),
        ),
        migrations.AddConstraint(
            model_name='plot',
            constraint=models.UniqueConstraint(fields=('visit', 'position'), name='observations_plot_visit_position_unique_relationships'),
        ),
        migrations.AddConstraint(
            model_name='identification',
            constraint=models.UniqueConstraint(fields=('observation', 'identification_guide', 'species', 'date_of_identification'), name='observations_identification_specimen_guide_species_date_unique_relationships'),
        ),
    ]

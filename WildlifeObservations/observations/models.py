from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Site(models.Model):
    area = models.CharField(max_length=30)
    site_name = models.CharField(max_length=5, unique=True)
    altitude_band = models.IntegerField(validators=[MinValueValidator(0)])

    gps_latitude_start = models.FloatField(null=True, blank=True,
                                           validators=[MinValueValidator(-90), MaxValueValidator(90)])
    gps_longitude_start = models.FloatField(null=True, blank=True,
                                            validators=[MinValueValidator(-180), MaxValueValidator(180)])
    gps_altitude_start = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    gps_number_satellites_start = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    gps_accuracy_start = models.IntegerField(null=True, blank=True)
    gps_aspect_start = models.FloatField(null=True, blank=True)

    gps_latitude_end = models.FloatField(null=True, blank=True,
                                         validators=[MinValueValidator(-90), MaxValueValidator(90)])
    gps_longitude_end = models.FloatField(null=True, blank=True,
                                          validators=[MinValueValidator(-180), MaxValueValidator(180)])
    gps_altitude_end = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    gps_number_satellites_end = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    gps_accuracy_end = models.IntegerField(null=True, blank=True)
    gps_aspect_end = models.FloatField(null=True, blank=True)

    transect_length = models.FloatField(null=True, blank=True,
                                        validators=[MinValueValidator(0), MaxValueValidator(100)])

    transect_description = models.TextField(max_length=2048, null=True, blank=True)

    notes = models.TextField(max_length=2048, null=True, blank=True)

    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} ({}m)".format(self.site_name, self.altitude_band)


class Visit(models.Model):

    site_name = models.ForeignKey(Site, on_delete=models.PROTECT)
    date = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('site_name', 'date',),)

    def __str__(self):
        return "{} {}".format(self.site_name, self.date)


class Survey(models.Model):

    class Method(models.TextChoices):
        NET = 'Net', _('Net')
        HAND = 'Hand', _('Hand')

    class Repeat(models.TextChoices):
        ONE = '1', _('1')
        TWO = '2', _('2')

    visit = models.ForeignKey(Visit, on_delete=models.PROTECT)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    method = models.CharField(max_length=5, choices=Method.choices, null=True, blank=True)
    repeat = models.CharField(max_length=2, choices=Repeat.choices, null=True, blank=True)
    observer = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {} {}".format(self.visit, self.method, self.repeat)

    class Meta:
        unique_together = (('visit', 'method', 'repeat',),)


class MeteorologyConditions(models.Model):
    survey = models.OneToOneField(Survey, on_delete=models.PROTECT, unique=True)
    cloud_coverage_start = models.IntegerField(null=True, blank=True,
                                               validators=[MinValueValidator(0), MaxValueValidator(8)])
    wind_start = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    rain_start = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    cloud_coverage_end = models.IntegerField(null=True, blank=True,
                                             validators=[MinValueValidator(0), MaxValueValidator(8)])
    wind_end = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    rain_end = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    notes = models.TextField(max_length=2048, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.survey)

    class Meta:
        verbose_name_plural = 'Meteorological conditions'


class Observation(models.Model):

    class Status(models.TextChoices):

        OBSERVED = 'Observed', _('Observed')
        SPECIMEN = 'Specimen', _('Specimen')
        LOST = 'Lost', _('Lost')

    specimen_id = models.CharField(max_length=22, unique=True, null=False, blank=False, validators=[
        RegexValidator(regex='^[A-Z]{3}[0-9]{2} [0-9]{8} [A-Z]{1}[0-9]{1} [A-Z]{1}[0-9]{3}$',
                       message='Format is sitename yyyymmdd methodrepeat specimen',
                       code='Invalid format')])
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    length_head_abdomen = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    length_head_tegmina = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=Status.choices, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.specimen_id)


class TaxonomyClass(models.Model):
    taxclass = models.CharField(max_length=255, unique=True, null=False, blank=False)

    def __str__(self):
        return "{}".format(self.taxclass)

    class Meta:
        verbose_name_plural = 'Taxonomy classes'


class TaxonomyOrder(models.Model):
    order = models.CharField(max_length=255, unique=True, null=False, blank=False)
    taxclass = models.ForeignKey(TaxonomyClass, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.order)

    class Meta:
        verbose_name_plural = 'Taxonomy orders'


class TaxonomySuborder(models.Model):
    suborder = models.CharField(max_length=20, null=False, blank=False, unique=True)
    order = models.ForeignKey(TaxonomyOrder, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.suborder)

    class Meta:
        verbose_name_plural = 'Taxonomy sub-orders'


class TaxonomyFamily(models.Model):
    family = models.CharField(max_length=20, null=False, blank=False, unique=True)
    suborder = models.ForeignKey(TaxonomySuborder, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.family)

    class Meta:
        verbose_name_plural = 'Taxonomy families'


class TaxonomySpecies(models.Model):
    latin_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    family = models.ForeignKey(TaxonomyFamily, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.latin_name)

    class Meta:
        verbose_name_plural = 'Taxonomy species'


class SpeciesName(models.Model):
    latin_name = models.OneToOneField(TaxonomySpecies, on_delete=models.PROTECT, unique=True)
    common_name_english = models.CharField(max_length=100, null=True, blank=True)
    common_name_catalan = models.CharField(max_length=100, null=True, blank=True)
    common_name_spanish = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.latin_name, self.common_name_english)

    class Meta:
        verbose_name_plural = 'Species names'


class IdentificationGuide(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False, unique=True)
    author = models.CharField(max_length=1024, null=False, blank=False)

    def __str__(self):
        return "{} - {}".format(self.author, self.title)


class Identification(models.Model):
    class Sex(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')
        UNKNOWN = 'Unknown', _('Unknown')

    class Stage(models.TextChoices):
        ADULT = 'Adult', _('Adult')
        NYMPH = 'Nymph', _('Nymph')
        UNKNOWN = 'Unknown', _('Unknown')

    class Confidence(models.TextChoices):
        IN_PROGRESS = 'In_progress', _('In progress')
        CHECK = 'Check', _('Check')
        CONFIRMED = 'Confirmed', _('Confirmed')
        REDO = 'Redo', _('Redo')

    specimen_id = models.ForeignKey(Observation, on_delete=models.PROTECT)
    species = models.ForeignKey(SpeciesName, on_delete=models.PROTECT, null=True, blank=True)
    identification_notes = models.TextField(max_length=2048, null=True, blank=True)
    identification_guide = models.ForeignKey(IdentificationGuide, on_delete=models.PROTECT, null=True, blank=True)
    sex = models.CharField(max_length=7, choices=Sex.choices, null=True, blank=True)
    stage = models.CharField(max_length=7, choices=Stage.choices, null=True, blank=True)
    confidence = models.CharField(max_length=11, choices=Confidence.choices, null=True, blank=True)
    date_of_identification = models.DateField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {} [{}]".format(self.specimen_id, self.species, self.confidence)

    class Meta:
        unique_together = (('specimen_id', 'identification_guide', 'species', 'date_of_identification'),)


class Plot(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.PROTECT)
    position = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} ({}m)".format(self.visit, self.position)


class VegetationStructure(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.PROTECT)
    percentage_vegetation_cover = models.IntegerField(null=True, blank=True,
                                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    percentage_bare_ground = models.IntegerField(null=True, blank=True,
                                                 validators=[MinValueValidator(0), MaxValueValidator(100)])
    percentage_rock = models.IntegerField(null=True, blank=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    height_75percent = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    max_height = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    density_01 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    density_02 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    density_03 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    density_04 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    density_05 = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    notes = models.TextField(max_length=2048, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.plot)

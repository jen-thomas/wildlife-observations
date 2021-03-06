from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Source(models.Model):
    class PositionSource(models.TextChoices):
        VIKINGTOPO = 'Viking Topo', _('Viking Topo')
        GPS = 'GPS', _('GPS')
        DEM = 'DEM', _('DEM')
        OSMAND = 'OsmAnd', _('OsmAnd')

    name = models.CharField(max_length=20, choices=PositionSource.choices)

    def __str__(self):
        return "{}".format(self.name)


class Site(models.Model):
    area = models.CharField(max_length=30)
    site_name = models.CharField(max_length=5, unique=True)
    altitude_band = models.IntegerField(validators=[MinValueValidator(0)])

    latitude_start = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    latitude_start_source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='+')
    longitude_start = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    longitude_start_source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='+')
    altitude_start = models.FloatField(validators=[MinValueValidator(0)])
    altitude_start_source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='+')

    gps_number_satellites_start = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    gps_accuracy_start = models.IntegerField(null=True, blank=True)
    gps_aspect_start = models.FloatField(null=True, blank=True)

    latitude_end = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    latitude_end_source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='+')
    longitude_end = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    longitude_end_source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='+')
    altitude_end = models.FloatField(validators=[MinValueValidator(0)])
    altitude_end_source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='+')

    gps_number_satellites_end = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    gps_accuracy_end = models.IntegerField(null=True, blank=True)
    gps_aspect_end = models.FloatField(null=True, blank=True)

    transect_length = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    transect_length_source = models.ForeignKey(Source, on_delete=models.PROTECT)

    transect_description = models.TextField(max_length=2048, default='', blank=True)

    notes = models.TextField(max_length=2048, default='', blank=True)

    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} ({}m)".format(self.site_name, self.altitude_band)


class Visit(models.Model):
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    date = models.DateField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [models.UniqueConstraint(
            name="%(app_label)s_%(class)s_site_date_unique_relationships",
            fields=['site', 'date'])]

    def __str__(self):
        return "{} {}".format(self.site, self.date)


class Survey(models.Model):
    class Method(models.TextChoices):
        NET = 'Net', _('Net')
        HAND = 'Hand', _('Hand')

    class Repeat(models.IntegerChoices):
        ONE = 1
        TWO = 2

    visit = models.ForeignKey(Visit, on_delete=models.PROTECT)
    start_time = models.TimeField()
    end_time = models.TimeField()
    method = models.CharField(max_length=5, choices=Method.choices)
    repeat = models.IntegerField(choices=Repeat.choices)
    observer = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {} {}".format(self.visit, self.method, self.repeat)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="%(app_label)s_%(class)s_visit_method_repeat_unique_relationships",
                                    fields=['visit', 'method', 'repeat']),
            models.UniqueConstraint(name="%(app_label)s_%(class)s_visit_start_unique_relationships",
                                    fields=['visit', 'start_time'])]


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
    notes = models.TextField(max_length=2048, default='', blank=True)
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

    class PreservationType(models.TextChoices):
        FROZEN = 'Frozen', _('Frozen')
        ALCOHOL = 'Alcohol', _('Alcohol')
        PINNED = 'Pinned', _('Pinned')
        NA = 'NA', _('NA')

    specimen_label = models.CharField(max_length=22, unique=True, validators=[
        RegexValidator(regex='^[A-Z]{3}[0-9]{2} [0-9]{8} [A-Z]{1}[0-9]{1} [A-Z]{1}[0-9]{3}$',
                       message='Format is sitename yyyymmdd methodrepeat specimen',
                       code='Invalid format')])
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    length_head_abdomen = models.FloatField(null=True, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    length_head_tegmina = models.FloatField(null=True, blank=True,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    original_preservation = models.CharField(max_length=10, choices=PreservationType.choices,
                                             default=PreservationType.FROZEN)
    current_preservation = models.CharField(max_length=10, choices=PreservationType.choices,
                                            default=PreservationType.FROZEN)
    status = models.CharField(max_length=10, choices=Status.choices)
    notes = models.TextField(max_length=1024, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.specimen_label)


class Photograph(models.Model):
    filepath = models.CharField(max_length=300, unique=True)
    observation = models.ManyToManyField(Observation)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.filepath)


class TaxonomyClass(models.Model):
    taxclass = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "{}".format(self.taxclass)

    class Meta:
        verbose_name_plural = 'Taxonomy classes'


class TaxonomyOrder(models.Model):
    order = models.CharField(max_length=255, unique=True)
    taxclass = models.ForeignKey(TaxonomyClass, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.order)

    class Meta:
        verbose_name_plural = 'Taxonomy orders'


class TaxonomySuborder(models.Model):
    suborder = models.CharField(max_length=255, unique=True)
    order = models.ForeignKey(TaxonomyOrder, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.suborder)

    class Meta:
        verbose_name_plural = 'Taxonomy sub-orders'


class TaxonomyFamily(models.Model):
    family = models.CharField(max_length=255, unique=True)
    suborder = models.ForeignKey(TaxonomySuborder, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.family)

    class Meta:
        verbose_name_plural = 'Taxonomy families'


class TaxonomySubfamily(models.Model):
    subfamily = models.CharField(max_length=255, unique=True)
    family = models.ForeignKey(TaxonomyFamily, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.subfamily)

    class Meta:
        verbose_name_plural = 'Taxonomy subfamilies'


class TaxonomyGenus(models.Model):
    genus = models.CharField(max_length=255, unique=True)
    subfamily = models.ForeignKey(TaxonomySubfamily, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.genus)

    class Meta:
        verbose_name_plural = 'Taxonomy genera'
        ordering = ['genus']


class TaxonomySpecies(models.Model):
    latin_name = models.CharField(max_length=255, unique=True)
    genus = models.ForeignKey(TaxonomyGenus, on_delete=models.PROTECT)
    common_name_english = models.CharField(max_length=100, null=True, blank=True)
    common_name_catalan = models.CharField(max_length=100, null=True, blank=True)
    common_name_spanish = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.latin_name)

    class Meta:
        verbose_name_plural = 'Taxonomy species'


class IdentificationGuide(models.Model):
    title = models.CharField(max_length=150, unique=True)
    author = models.CharField(max_length=1024)

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
        CHECK_IN_MUSEUM = 'Check_in_museum', _('Check in museum')
        CONFIRMED = 'Confirmed', _('Confirmed')
        REDO = 'Redo', _('Redo')
        REVIEW = 'Review', _('Review')
        FINALISED = 'Finalised', _('Finalised')

    class ConfidenceReason(models.TextChoices):
        ID_CERTAIN = 'ID_certain', _('ID certain')
        ID_UNCERTAIN = 'ID_uncertain', _('ID uncertain')
        ID_INCOMPLETE = 'ID_incomplete', _('ID incomplete')
        ID_NEEDS_CONFIRMATION = 'ID_needs_confirmation', _('ID needs confirmation')
        ID_INCORRECT = 'ID_incorrect', _('ID incorrect')
        CANNOT_DETERMINE_FURTHER = 'Cannot_determine_further', _('Cannot determine further')
        SMALL_NYMPH_HARD_TO_ID = 'Small_nymph_hard_to_ID', _('Small nymph hard to ID')
        CANNOT_SPLIT_FURTHER = 'Cannot_split_further', _('Cannot split further')

    observation = models.ForeignKey(Observation, on_delete=models.PROTECT)
    species = models.ForeignKey(TaxonomySpecies, on_delete=models.PROTECT, null=True, blank=True)
    genus = models.ForeignKey(TaxonomyGenus, on_delete=models.PROTECT, null=True, blank=True)
    subfamily = models.ForeignKey(TaxonomySubfamily, on_delete=models.PROTECT, null=True, blank=True)
    family = models.ForeignKey(TaxonomyFamily, on_delete=models.PROTECT, null=True, blank=True)
    suborder = models.ForeignKey(TaxonomySuborder, on_delete=models.PROTECT, null=True, blank=True)
    identification_notes = models.TextField(max_length=2048, null=True, blank=True)
    identification_guide = models.ForeignKey(IdentificationGuide, on_delete=models.PROTECT, null=True, blank=True)
    sex = models.CharField(max_length=7, choices=Sex.choices, null=True, blank=True)
    stage = models.CharField(max_length=7, choices=Stage.choices, null=True, blank=True)
    confidence = models.CharField(max_length=30, choices=Confidence.choices, null=True, blank=True)
    confidence_reason = models.CharField(max_length=30, choices=ConfidenceReason.choices, null=True, blank=True)
    date_of_identification = models.DateField(null=True, blank=True)
    notebook = models.CharField(max_length=10)
    comments = models.TextField(max_length=1000, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.species is not None:
            self.genus = self.species.genus

        if self.genus is not None:
            self.subfamily = self.genus.subfamily

        if self.subfamily is not None:
            self.family = self.subfamily.family

        if self.family is not None:
            self.suborder = self.family.suborder

        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {} [{}]".format(self.observation, self.species, self.confidence)

    class Meta:
        constraints = [models.UniqueConstraint(
            name="%(app_label)s_%(class)s_specimen_guide_species_date_unique_relationships",
            fields=['observation', 'identification_guide', 'species', 'date_of_identification']),

            # add constraints to ensure only allowed combinations of confidence and confidence reason
            models.CheckConstraint(name="%(app_label)s_%(class)s_check_confidence_reasons",
                                   check=Q(Q(confidence='Confirmed') & Q(confidence_reason__in=(
                                   'Small_nymph_hard_to_ID', 'Cannot_determine_further', 'ID_certain')))
                                         | Q(Q(confidence__in=('Check', 'Check_in_museum')) &
                                           Q(confidence_reason='ID_needs_confirmation'))
                                         | Q(Q(confidence='In_progress') & Q(confidence_reason='ID_incomplete'))
                                         | Q(Q(confidence='Review') & Q(confidence_reason='ID_uncertain'))
                                         | Q(Q(confidence='Redo') & Q(confidence_reason='ID_incorrect'))
                                         | Q(Q(confidence='Finalised') & Q(confidence_reason='Cannot_split_further'))
                                   )]


class Plot(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.PROTECT)
    position = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} ({}m)".format(self.visit, self.position)

    class Meta:
        constraints = [models.UniqueConstraint(
            name="%(app_label)s_%(class)s_visit_position_unique_relationships",
            fields=['visit', 'position'])]


class VegetationStructure(models.Model):
    plot = models.OneToOneField(Plot, on_delete=models.PROTECT)
    percentage_vegetation_cover = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    percentage_bare_ground = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    percentage_rock = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    height_75percent = models.IntegerField(validators=[MinValueValidator(0)])
    max_height = models.IntegerField(validators=[MinValueValidator(0)])
    density_01 = models.IntegerField(validators=[MinValueValidator(0)])
    density_02 = models.IntegerField(validators=[MinValueValidator(0)])
    density_03 = models.IntegerField(validators=[MinValueValidator(0)])
    density_04 = models.IntegerField(validators=[MinValueValidator(0)])
    density_05 = models.IntegerField(validators=[MinValueValidator(0)])
    notes = models.TextField(max_length=2048, default='', blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.plot)

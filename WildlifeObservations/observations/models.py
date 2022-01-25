from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Site(models.Model):

    area = models.CharField(max_length=30)
    site_name = models.CharField(max_length=5)
    altitude_band = models.IntegerField()
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.site_name)


class Visit(models.Model):

    class Method(models.TextChoices):
        NET = 'Net', _('Net')
        HAND = 'Hand', _('Hand')

    class Repeat(models.TextChoices):
        ONE = '1', _('1')
        TWO = '2', _('2')

    site_name = models.ForeignKey(Site, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    method = models.CharField(max_length=5, choices=Method.choices)
    repeat = models.CharField(max_length=2, choices=Repeat.choices)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {} {}{}".format(self.site_name, self.date, self.method, self.repeat)


class Observation(models.Model):

    specimen_id = models.CharField(max_length=22, unique=True, null=False, blank=False)
    visit = models.ForeignKey(Visit, on_delete=models.PROTECT)
    length_head_abdomen = models.FloatField(null=True, blank=True)
    length_head_tegmina = models.FloatField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.specimen_id)


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

    latin_name = models.CharField(max_length=255, unique=True)
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
        return "{}".format(self.common_name_english)

    class Meta:
        verbose_name_plural = 'Species names'


class IdentificationGuide(models.Model):

    title = models.CharField(max_length=150, null=False, blank=False)
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

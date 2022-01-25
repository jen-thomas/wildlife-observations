from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Site(models.Model):
    area = models.CharField(max_length=30)
    site_name = models.CharField(max_length=5)
    altitude_band = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

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

    def __str__(self):
        return "{} {} {}{}".format(self.site_name, self.date, self.method, self.repeat)


class Observation(models.Model):

    specimen_id = models.CharField(max_length=22, unique=True, null=False, blank=False)
    visit = models.ForeignKey(Visit, on_delete=models.PROTECT)
    length_head_abdomen = models.FloatField()
    length_head_tegmina = models.FloatField()

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


class Taxonomy(models.Model):
    latin_name = models.CharField(max_length=255, unique=True)
    order = models.ForeignKey(TaxonomyOrder, on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.latin_name)

    class Meta:
        verbose_name_plural = 'Taxonomies'


class Species(models.Model):
    latin_name = models.OneToOneField(Taxonomy, on_delete=models.PROTECT, unique=True)
    common_name_english = models.CharField(max_length=1024, null=True, blank=True)
    common_name_catalan = models.CharField(max_length=1024, null=True, blank=True)
    common_name_spanish = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.common_name_english)

    class Meta:
        verbose_name_plural = 'Species'


class Identification(models.Model):

    class Sex(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')

    class Stage(models.TextChoices):
        ADULT = 'Adult', _('Adult')
        NYMPH = 'Nymph', _('Nymph')

    class Confidence(models.TextChoices):
        IN_PROGRESS = 'In_progress', _('In progress')
        CHECK = 'Check', _('Check')
        CONFIRMED = 'Confirmed', _('Confirmed')
        REDO = 'Redo', _('Redo')

    specimen_id = models.ForeignKey(Observation, on_delete=models.PROTECT)
    species = models.CharField(max_length=20)
    identification_notes = models.TextField(max_length=2048)
    identification_guide = models.CharField(max_length=20)
    sex = models.CharField(max_length=6, choices=Sex.choices)
    stage = models.CharField(max_length=5, choices=Stage.choices)
    confidence = models.CharField(max_length=11, choices=Confidence.choices)

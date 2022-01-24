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

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



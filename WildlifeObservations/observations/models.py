from django.db import models
from django.conf import settings
from django.utils import timezone


class Site(models.Model):
    area = models.CharField(max_length=30)
    site_name = models.CharField(max_length=5)
    altitude_band = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.site_name

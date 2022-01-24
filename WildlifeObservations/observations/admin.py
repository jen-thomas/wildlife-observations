from django.contrib import admin
from . import models


# Register your models here.

class SiteAdmin(admin.ModelAdmin):
    list_display = ('area', 'site_name', 'altitude_band',)
    ordering = ('site_name', 'altitude_band',)
    search_fields = ('area', 'site_name', 'altitude_band',)


class VisitAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'date', 'start_time', 'end_time', 'method', 'repeat',)
    ordering = ('site_name', 'date', 'start_time', 'end_time',)
    search_fields = ('site_name', 'date', 'start_time', 'end_time', 'method',)


class ObservationAdmin(admin.ModelAdmin):
    list_display = ('specimen_id', 'visit', 'length_head_abdomen', 'length_head_tegmina',)
    ordering = ('specimen_id', 'visit',)
    search_fields = ('specimen_id', 'visit', 'length_head_abdomen',)


class IdentificationAdmin(admin.ModelAdmin):
    list_display = ('specimen_id', 'species', 'identification_guide', 'sex', 'stage', 'confidence',)
    ordering = ('specimen_id', 'species', 'identification_guide', 'sex', 'stage', 'confidence',)
    search_fields = ('specimen_id', 'species', 'identification_guide', 'sex', 'stage', 'confidence',)


admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Visit, VisitAdmin)
admin.site.register(models.Observation, ObservationAdmin)
admin.site.register(models.Identification, IdentificationAdmin)

from django.contrib import admin
from . import models


# Register your models here.

class SiteAdmin(admin.ModelAdmin):
    list_display = ('area', 'site_name', 'altitude_band', 'gps_latitude_start', 'gps_longitude_start', 'gps_altitude_start', 'gps_aspect_start', 'gps_latitude_end', 'gps_longitude_end', 'gps_altitude_end', 'gps_aspect_end', 'transect_length',)
    ordering = ('site_name', 'altitude_band', 'gps_altitude_start', 'gps_altitude_end', 'gps_aspect_start', 'gps_aspect_end', 'transect_length',)
    search_fields = ('area', 'site_name', 'altitude_band', 'transect_length',)


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


class TaxonomyClassAdmin(admin.ModelAdmin):
    list_display = ('taxclass',)
    ordering = ('taxclass',)
    search_fields = ('taxclass',)


class TaxonomyOrderAdmin(admin.ModelAdmin):
    list_display = ('taxclass', 'order',)
    ordering = ('taxclass', 'order',)
    search_fields = ('taxclass', 'order',)


class TaxonomySuborderAdmin(admin.ModelAdmin):
    list_display = ('order', 'suborder',)
    ordering = ('order', 'suborder',)
    search_fields = ('order', 'suborder',)


class TaxonomyFamilyAdmin(admin.ModelAdmin):
    list_display = ('suborder', 'family',)
    ordering = ('suborder', 'family',)
    search_fields = ('suborder', 'family',)


class TaxonomySpeciesAdmin(admin.ModelAdmin):
    list_display = ('family', 'latin_name',)
    ordering = ('family', 'latin_name',)
    search_fields = ('family', 'latin_name',)


class SpeciesNameAdmin(admin.ModelAdmin):
    list_display = ('latin_name', 'common_name_english', 'common_name_catalan', 'common_name_spanish',)
    ordering = ('latin_name', 'common_name_english', 'common_name_catalan', 'common_name_spanish',)
    search_fields = ('latin_name', 'common_name_english', 'common_name_catalan', 'common_name_spanish',)


class IdentificationGuideAdmin(admin.ModelAdmin):
    list_display = ('author', 'title',)
    ordering = ('author', 'title',)
    search_fields = ('author', 'title',)


class MeteorologyConditionsAdmin(admin.ModelAdmin):
    list_display = ('visit', 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end', 'rain_end', 'notes',)
    ordering = ('visit', 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end', 'rain_end',)
    search_fields = ('visit', 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end', 'rain_end',)


admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Visit, VisitAdmin)
admin.site.register(models.Observation, ObservationAdmin)
admin.site.register(models.Identification, IdentificationAdmin)
admin.site.register(models.TaxonomyClass, TaxonomyClassAdmin)
admin.site.register(models.TaxonomyOrder, TaxonomyOrderAdmin)
admin.site.register(models.TaxonomySuborder, TaxonomySuborderAdmin)
admin.site.register(models.TaxonomyFamily, TaxonomyFamilyAdmin)
admin.site.register(models.TaxonomySpecies, TaxonomySpeciesAdmin)
admin.site.register(models.SpeciesName, SpeciesNameAdmin)
admin.site.register(models.IdentificationGuide, IdentificationGuideAdmin)
admin.site.register(models.MeteorologyConditions, MeteorologyConditionsAdmin)
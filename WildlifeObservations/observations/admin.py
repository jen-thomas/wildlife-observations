from django.contrib import admin
from django import forms

from . import models

# Register your models here.
from .models import VegetationStructure, Survey


class SiteAdmin(admin.ModelAdmin):
    list_display = (
        'area', 'site_name', 'altitude_band', 'gps_latitude_start', 'gps_longitude_start', 'gps_altitude_start',
        'gps_aspect_start', 'gps_latitude_end', 'gps_longitude_end', 'gps_altitude_end', 'gps_aspect_end',
        'transect_length',)
    ordering = (
        'site_name', 'altitude_band', 'gps_altitude_start', 'gps_altitude_end', 'gps_aspect_start', 'gps_aspect_end',
        'transect_length',)
    search_fields = ('area', 'site_name', 'altitude_band', 'transect_length',)


class VisitAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'date',)
    ordering = ('site_name', 'date',)
    search_fields = ('site_name__site_name', 'date',)


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('visit', 'start_time', 'end_time', 'method', 'repeat', 'observer',)
    ordering = ('visit', 'start_time', 'end_time', 'method', 'repeat',)
    search_fields = ('visit__site_name', 'start_time', 'end_time', 'method', 'observer',)


class ObservationAdmin(admin.ModelAdmin):
    list_display = ('specimen_label', 'survey', 'status', 'length_head_abdomen', 'length_head_tegmina',)
    ordering = ('specimen_label', 'survey', 'status',)
    search_fields = ('specimen_label', 'survey__visit', 'status', 'length_head_abdomen',)


class IdentificationAdmin(admin.ModelAdmin):
    list_display = (
    'specimen_label', 'species', 'specimen_status', 'identification_guide', 'sex', 'stage', 'confidence',)
    ordering = ('specimen_label', 'species', 'identification_guide', 'sex', 'stage', 'confidence',)
    search_fields = (
    'specimen_label__specimen_label', 'species', 'identification_guide__title', 'sex', 'stage', 'confidence',)

    def specimen_status(self, obj):
        return "{}".format(obj.specimen_label.status)


class TaxonomyClassAdmin(admin.ModelAdmin):
    list_display = ('taxclass',)
    ordering = ('taxclass',)
    search_fields = ('taxclass',)


class TaxonomyOrderAdmin(admin.ModelAdmin):
    list_display = ('taxclass', 'order',)
    ordering = ('taxclass', 'order',)
    search_fields = ('taxclass__taxclass', 'order',)


class TaxonomySuborderAdmin(admin.ModelAdmin):
    list_display = ('order', 'suborder',)
    ordering = ('order', 'suborder',)
    search_fields = ('order__order', 'suborder',)


class TaxonomyFamilyAdmin(admin.ModelAdmin):
    list_display = ('suborder', 'family',)
    ordering = ('suborder', 'family',)
    search_fields = ('suborder__suborder', 'family',)


class TaxonomySpeciesAdmin(admin.ModelAdmin):
    list_display = ('family', 'latin_name', 'common_name_english', 'common_name_catalan', 'common_name_spanish',)
    ordering = ('family', 'latin_name', 'common_name_english', 'common_name_catalan', 'common_name_spanish',)
    search_fields = (
    'family__family', 'latin_name', 'common_name_english', 'common_name_catalan', 'common_name_spanish',)


class IdentificationGuideAdmin(admin.ModelAdmin):
    list_display = ('author', 'title',)
    ordering = ('author', 'title',)
    search_fields = ('author', 'title',)


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = "__all__"

    # def clean(self):
    #     if self.cleaned_data['repeat'] > 1 and Survey.objects.get('method' == self.cleaned_data['method'])['repeat'] != self.cleaned_data['repeat']-1:
    #         raise forms.ValidationError("Check there is an earlier repeat using this survey method")
    #
    #     return self.cleaned_data


class MeteorologyConditionsAdmin(admin.ModelAdmin):
    list_display = (
        'survey', 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end', 'rain_end',
        'notes',)
    ordering = (
        'survey', 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end', 'rain_end',)
    search_fields = (
        'survey__visit', 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end',
        'rain_end',)


class PlotAdmin(admin.ModelAdmin):
    list_display = ('visit', 'position',)
    ordering = ('visit', 'position',)
    search_fields = ('visit__visit', 'position',)


class VegetationStructureForm(forms.ModelForm):
    class Meta:
        model = VegetationStructure
        fields = "__all__"

    def clean(self):
        if self.cleaned_data['percentage_rock'] + self.cleaned_data['percentage_bare_ground'] + self.cleaned_data[
            'percentage_vegetation_cover'] != 100:
            raise forms.ValidationError("Ground cover percentages do not add up to 100")

        return self.cleaned_data


class VegetationStructureAdmin(admin.ModelAdmin):
    form = VegetationStructureForm
    list_display = (
        'plot', 'percentage_vegetation_cover', 'percentage_bare_ground', 'percentage_rock', 'height_75percent',
        'max_height', 'density_01', 'density_02', 'density_03', 'density_04', 'density_05',)
    ordering = ('plot', 'percentage_vegetation_cover', 'percentage_bare_ground', 'percentage_rock', 'height_75percent',
                'max_height', 'density_01', 'density_02', 'density_03', 'density_04', 'density_05',)
    search_fields = (
        'plot__plot', 'percentage_vegetation_cover', 'percentage_bare_ground', 'percentage_rock', 'height_75percent',
        'max_height', 'density_01', 'density_02', 'density_03', 'density_04', 'density_05',)


admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Visit, VisitAdmin)
admin.site.register(models.Observation, ObservationAdmin)
admin.site.register(models.Identification, IdentificationAdmin)
admin.site.register(models.TaxonomyClass, TaxonomyClassAdmin)
admin.site.register(models.TaxonomyOrder, TaxonomyOrderAdmin)
admin.site.register(models.TaxonomySuborder, TaxonomySuborderAdmin)
admin.site.register(models.TaxonomyFamily, TaxonomyFamilyAdmin)
admin.site.register(models.TaxonomySpecies, TaxonomySpeciesAdmin)
admin.site.register(models.IdentificationGuide, IdentificationGuideAdmin)
admin.site.register(models.MeteorologyConditions, MeteorologyConditionsAdmin)
admin.site.register(models.Plot, PlotAdmin)
admin.site.register(models.VegetationStructure, VegetationStructureAdmin)
admin.site.register(models.Survey, SurveyAdmin)

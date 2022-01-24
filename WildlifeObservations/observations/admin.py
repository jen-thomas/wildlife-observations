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


admin.site.register(models.Site, SiteAdmin)

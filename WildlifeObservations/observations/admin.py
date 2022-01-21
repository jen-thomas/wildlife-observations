from django.contrib import admin
from . import models

# Register your models here.

class SiteAdmin(admin.ModelAdmin):
    list_display = ('area', 'site_name', 'altitude_band',)
    ordering = ('site_name', 'altitude_band',)
    search_fields = ('area', 'site_name', 'altitude_band',)

admin.site.register(models.Site, SiteAdmin)


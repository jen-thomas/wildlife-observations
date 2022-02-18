from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Site
import csv


class Command(BaseCommand):
    help = 'Adds sites'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        print(options['filename'])
        self.import_data_from_csv(options['filename'])

    def import_data_from_csv(self, filename):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                site = Site()
                site.area = row['area']
                site.site_name = row['sitename']
                site.altitude_band = row['altitude_band']
                site.transect_length = row['transect_length']
                site.transect_description = row['transect_description']
                site.notes = row['notes']

                site.latitude_start = row['start_latitude']
                site.longitude_start = row['start_longitude']
                site.altitude_start = row['start_altitude']

                if row['start_number_satellites'] != '':
                    site.gps_number_satellites_start = row['start_number_satellites']
                if row['start_gps_accuracy'] != '':
                    site.gps_accuracy_start = row['start_gps_accuracy']
                if row['start_orientation'] != '':
                    site.gps_aspect_start = row['start_orientation']

                site.latitude_end = row['end_latitude']
                site.longitude_end = row['end_longitude']
                site.altitude_end = row['end_altitude']

                if row['end_number_satellites'] != '':
                    site.gps_number_satellites_end = row['end_number_satellites']
                if row['end_gps_accuracy'] != '':
                    site.gps_accuracy_end = row['end_gps_accuracy']
                if row['end_orientation'] != '':
                    site.gps_aspect_end = row['end_orientation']

                site.save()
import argparse
import csv

from django.core.management.base import BaseCommand

from ...models import Site

header_site = ['area', 'site_name', 'elevational_band_m', 'latitude_start_n', 'longitude_start_e', 'elevation_start_m',
               'latitude_end_n', 'longitude_end_e', 'elevation_end_m', 'transect_length_m']


def export_csv(output_file):
    """
    Export data from a query into a CSV file which has a specified output file.

    Using an ORM query, get some data from the database and export specified fields into a CSV file which uses a set
    of headers.
    """

    headers = header_site

    csv_writer = csv.DictWriter(output_file, headers)
    csv_writer.writeheader()

    sites = Site.objects.all().order_by('area', 'altitude_band')

    for site in sites:
        row = {}

        row['area'] = site.area
        row['site_name'] = site.site_name
        row['elevational_band_m'] = site.altitude_band
        row['latitude_start_n'] = site.latitude_start
        row['longitude_start_e'] = site.longitude_start
        row['elevation_start_m'] = site.altitude_start
        row['latitude_end_n'] = site.latitude_end
        row['longitude_end_e'] = site.longitude_end
        row['elevation_end_m'] = site.altitude_end
        row['transect_length_m'] = site.transect_length

        csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        export_csv(options['output_file'])
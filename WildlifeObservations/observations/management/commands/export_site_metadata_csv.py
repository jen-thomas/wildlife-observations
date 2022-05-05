import argparse
import csv

from django.core.management.base import BaseCommand

from ...models import Site

header_site = ['area', 'site_name', 'altitude_band_m', 'altitude_start_source']


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
        row['altitude_band_m'] = site.altitude_band

        csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        export_csv(options['output_file'])
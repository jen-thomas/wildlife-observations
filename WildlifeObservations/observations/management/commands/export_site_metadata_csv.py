import csv

from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict

from ...models import Site

header_site = ['area', 'site_name', 'altitude_band']


def export_csv(file_path):
    with open(file_path, 'w') as file:
        headers = header_site

        csv_writer = csv.DictWriter(file, headers)

        csv_writer.writeheader()

        sites = Site.objects.all().order_by('area', 'altitude_band')

        for site in sites:
            row = {}

            row['area'] = site.area
            row['site_name'] = site.site_name
            row['altitude_band'] = site.altitude_band

            csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        file_path = options['file']

        if file_path == '-':
            file_path = '/dev/stdout'

        export_csv(file_path)
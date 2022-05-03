import csv

from django.core.management.base import BaseCommand

from ...models import Site

header_site = ['area', 'site_name', 'altitude_band_m']


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
            row['altitude_band_m'] = site.altitude_band

            csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_directory', type=str, help='Path to the file or - for stdout')
        parser.add_argument('file_basename', type=str, help='File basename')

    def handle(self, *args, **options):
        path = options['output_directory']
        file_name = options['file_basename']
        file_path = f'{path}/{file_name}.csv'

        if file_path == '-':
            file_path = '/dev/stdout'

        export_csv(file_path)
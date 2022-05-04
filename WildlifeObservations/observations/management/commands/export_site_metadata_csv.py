import csv

from django.core.management.base import BaseCommand

from ...models import Site

header_site = ['area', 'site_name', 'altitude_band_m', 'altitude_start_source']


def field_or_na(model, field_name):
    if model is None:
        return ''
    else:
        return getattr(model, field_name)

def export_csv(file_path):
    """
    Export data from a query into a CSV file which has a specified path and filename.

    Using an ORM query, get some data from the database and export specified fields into a CSV file which uses a set
    of headers.
    """

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

            row['altitude_start_source'] = field_or_na(site.altitude_start_source, 'name')



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
import csv

from django.core.management.base import BaseCommand

from ...models import VegetationStructure, Plot

header_survey = []


def export_csv(file_path):
    """
    Export data from a query into a CSV file which has a specified path and filename.

    Using an ORM query, get some data from the database and export specified fields into a CSV file which uses a set
    of headers.
    """

    with open(file_path, 'w') as file:
        headers = header_survey

        csv_writer = csv.DictWriter(file, headers)

        csv_writer.writeheader()

        vegetation_surveys = VegetationStructure.objects.all().order_by('')

        for survey in vegetation_surveys:
            row = {}

            row['site_name'] = survey.visit.site.site_name
            row['date_cest'] = survey.visit.date


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
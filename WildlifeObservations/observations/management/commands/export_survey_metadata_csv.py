import csv

from django.core.management.base import BaseCommand

from ...models import Survey, MeteorologyConditions

header_survey = ['site_name', 'date_cest', 'start_time_cest', 'end_time_cest', 'method', 'repeat',
                 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end', 'rain_end']


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

        surveys = Survey.objects.all().order_by('visit__site__site_name', 'visit__date', 'start_time')

        for survey in surveys:
            row = {}

            row['site_name'] = survey.visit.site.site_name
            row['date_cest'] = survey.visit.date
            row['start_time_cest'] = survey.start_time
            row['end_time_cest'] = survey.end_time
            row['method'] = survey.method
            row['repeat'] = survey.repeat
            row['cloud_coverage_start'] = MeteorologyConditions.cloud_coverage_start # TODO correct this
            row['wind_start'] = MeteorologyConditions.wind_start
            row['rain_start'] = MeteorologyConditions.rain_start
            row['cloud_coverage_end'] = MeteorologyConditions.cloud_coverage_end
            row['wind_end'] = MeteorologyConditions.wind_end
            row['rain_end'] = MeteorologyConditions.rain_end

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
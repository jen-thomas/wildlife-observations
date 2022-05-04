import argparse
import csv

from django.core.management.base import BaseCommand

from ...models import Survey, MeteorologyConditions

header_survey = ['site_name', 'date_cest', 'start_time_cest', 'end_time_cest', 'method', 'repeat',
                 'cloud_coverage_start', 'wind_start', 'rain_start', 'cloud_coverage_end', 'wind_end', 'rain_end']


def export_csv(output_file):
    """
    Export data from a query into a CSV file which has a specified path and filename.

    Using an ORM query, get some data from the database and export specified fields into a CSV file which uses a set
    of headers.
    """

    headers = header_survey

    csv_writer = csv.DictWriter(output_file, headers)

    csv_writer.writeheader()

    surveys = Survey.objects.all().order_by('visit__site__site_name', 'visit__date', 'start_time')

    for survey in surveys:

        survey_site_name = survey.visit.site.site_name
        survey_date = survey.visit.date

        row = {}

        row['site_name'] = survey_site_name
        row['date_cest'] = survey_date
        row['start_time_cest'] = survey.start_time
        row['end_time_cest'] = survey.end_time
        row['method'] = survey.method
        row['repeat'] = survey.repeat
        row['cloud_coverage_start'] = survey.meteorologyconditions.cloud_coverage_start
        row['wind_start'] = survey.meteorologyconditions.wind_start
        row['rain_start'] = survey.meteorologyconditions.rain_start
        row['cloud_coverage_end'] = survey.meteorologyconditions.cloud_coverage_end
        row['wind_end'] = survey.meteorologyconditions.wind_end
        row['rain_end'] = survey.meteorologyconditions.rain_end

        csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        export_csv(options['output_file'])
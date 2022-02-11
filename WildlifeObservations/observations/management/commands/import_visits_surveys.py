from django.core.management.base import BaseCommand

from ...models import Visit, Survey, MeteorologyConditions
import csv


class Command(BaseCommand):
    help = 'Adds visits'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        print(options['filename'])
        self.import_visit_from_csv(options['filename'])

    def import_met_conditions_from_csv(self, row, survey):

        met_conditions = MeteorologyConditions

        met_conditions.cloud_coverage_start = row['start_cloud']
        met_conditions.rain_start = row['start_rain']
        met_conditions.wind_start = row['start_wind']
        met_conditions.cloud_coverage_end = row['end_cloud']
        met_conditions.rain_end = row['end_rain']
        met_conditions.wind_end = row['end_wind']
        met_conditions.notes = row['notes']

        met_conditions.save()

        return met_conditions

    def import_survey_from_csv(self, row, visit):

        survey = Survey()

        survey.start_time = row['start_time']
        survey.end_time = row['end_time']
        survey.method = row['method']
        survey.repeat = row['repeat']

        survey.save()

        return survey

    def import_visit_from_csv(self, filename):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                visit = Visit()

                visit.site_name = row['sitename']
                visit.date = row['date']

                visit.save()

                survey = self.import_survey_from_csv(row, visit)

                self.import_met_conditions_from_csv(row, survey)


from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Visit, Survey, MeteorologyConditions, Site
import csv


class Command(BaseCommand):
    help = 'Adds visits'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        print(options['filename'])
        self.import_visit_from_csv(options['filename'])

    def import_met_conditions_from_csv(self, row_data, survey):
        met_conditions = MeteorologyConditions()

        met_conditions.survey = survey
        met_conditions.cloud_coverage_start = row_data['start_cloud']
        met_conditions.rain_start = row_data['start_rain']
        met_conditions.wind_start = row_data['start_wind']
        met_conditions.cloud_coverage_end = row_data['end_cloud']
        met_conditions.rain_end = row_data['end_rain']
        met_conditions.wind_end = row_data['end_wind']
        met_conditions.notes = row_data['notes']

        met_conditions.save()

        return met_conditions

    def import_survey_from_csv(self, row_data, visit):
        survey = Survey()

        survey.visit = visit
        survey.start_time = row_data['start_time']
        survey.end_time = row_data['end_time']
        survey.repeat = row_data['repeat']
        survey.observer = 'Jen Thomas' # all of the surveys were done by the same person in this case

        if row_data['method'] == 'net':
            survey.method = Survey.Method.NET
        elif row_data['method'] == 'hand':
            survey.method = Survey.Method.HAND

        if row_data['repeat'] == '1':
            survey.repeat = Survey.Repeat.ONE
        elif row_data['repeat'] == '2':
            survey.repeat = Survey.Repeat.TWO

        survey.save()

        return survey

    def import_visit_from_csv(self, filename):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                visit, created = Visit.objects.get_or_create(site=Site.objects.get(site_name=row['sitename']), date=row['date'])

                visit.save()

                survey_data = select_columns(row, ["start_time", "end_time", "method", "repeat"])
                survey = self.import_survey_from_csv(survey_data, visit)

                met_conditions_data = select_columns(row, ["start_cloud", "start_rain", "start_wind", "end_cloud",
                                                           "end_rain", "end_wind", "notes"])
                self.import_met_conditions_from_csv(met_conditions_data, survey)


def select_columns(row, list_of_columns) -> dict:
    selected = {}

    for column_name in list_of_columns:
        selected[column_name] = row[column_name]

    return selected

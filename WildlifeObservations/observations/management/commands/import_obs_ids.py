from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime


from ...models import Survey, Observation, IdentificationGuide, Identification, Visit, Site
import csv


class Command(BaseCommand):
    help = 'Adds observations and identifications'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        print(options['filename'])
        self.import_observation_from_csv(options['filename'])

    def import_observation_from_csv(self, filename):

        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                observation = Observation()

                survey_details = row['specimen_id'].split(' ')
                site = survey_details[0]

                visit_date = survey_details[1]
                visit_date_time_obj = datetime.strptime(visit_date, '%Y%m%d').date()

                survey_method = survey_details[2][0]
                if survey_method == 'N':
                    method = Survey.Method.NET
                elif survey_method == 'H':
                    method = Survey.Method.HAND

                survey_repeat = survey_details[2][1]

                visit = Visit.objects.get(site=Site.objects.get(site_name=site), date=visit_date_time_obj)
                survey = Survey.objects.get(visit=visit, method=method, repeat=survey_repeat)

                observation.specimen_label = row['specimen_id']
                observation.survey = survey

                if row['length_mm'] != '': # if nothing is assigned it is None by default
                    observation.length_head_abdomen = row['length_mm']

                observation.status = 'Specimen' # all those imported are specimens rather than observations

                observation.save()


def select_columns(row, list_of_columns) -> dict:
    selected = {}

    for column_name in list_of_columns:
        selected[column_name] = row[column_name]

    return selected
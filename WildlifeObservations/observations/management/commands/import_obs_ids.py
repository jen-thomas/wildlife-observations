from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime

from ...models import Survey, Observation, IdentificationGuide, Identification, Visit, Site, TaxonomySpecies
import csv


class Command(BaseCommand):
    help = 'Adds observations and identifications'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        print(options['filename'])
        self.import_observation_from_csv(options['filename'])

    def import_observation_from_csv(self, row_data, observation):
        identification = Identification()

        identification.observation = observation
        identification.species = TaxonomySpecies.objects.get(latin_name=row_data['species'])
        identification.identification_notes = row_data['id_notes']

        if row_data['guide'] == 'Sardet et al':
            identification.identification_guide = IdentificationGuide.objects.get(author='Sardet, Roesti and Braud')
        elif row_data['guide'] != '':
            identification.identification_guide = IdentificationGuide.objects.get(author=row_data['guide'])

        if row_data['sex'] == 'female':
            identification.sex = Identification.Sex.FEMALE
        elif row_data['sex'] == 'male':
            identification.sex = Identification.Sex.MALE
        elif row_data['sex'] == '':
            identification.sex = Identification.Sex.UNKNOWN

        if row_data['stage'] == 'adult':
            identification.stage = Identification.Stage.ADULT
        elif row_data['stage'] == 'nymph':
            identification.stage = Identification.Stage.NYMPH
        elif row_data['stage'] == '':
            identification.stage = Identification.Stage.UNKNOWN

        if row_data['sure'] == 'yes':
            identification.confidence = Identification.Confidence.YES
        elif row_data['sure'] == 'redo':
            identification.confidence = Identification.Confidence.REDO
        elif row_data['sure'] == 'check':
            identification.confidence = Identification.Confidence.CHECK
        elif row_data['sure'] == 'not finished':
            identification.confidence = Identification.Confidence.IN_PROGRESS
        elif row_data['sure'] == 'review':
            identification.confidence = Identification.Confidence.REVIEW
        elif row_data['sure'] == '':
            identification.confidence = Identification.Confidence.REVIEW

        if row_data['id_date'] != '':
            identification.date_of_identification = datetime.strptime(row_data['id_date'], '%Y-%m-%d').date()

        identification.notebook = row_data['notebook']
        identification.comments = row_data['comments']

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

                if row['length_mm'] != '':  # if nothing is assigned it is None by default
                    observation.length_head_abdomen = row['length_mm']

                observation.status = 'Specimen'  # all those imported are specimens rather than observations

                observation.save()

                identification_data = select_columns(row, ["genus", "species", "id_notes", "sure", "sex", "stage", "guide", "notebook", "id_date", "comments"])

                self.import_observation_from_csv(identification_data, observation)


def select_columns(row, list_of_columns) -> dict:
    selected = {}

    for column_name in list_of_columns:
        selected[column_name] = row[column_name]

    return selected

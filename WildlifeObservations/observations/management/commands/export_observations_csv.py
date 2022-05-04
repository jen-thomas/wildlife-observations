import csv

from django.core.management.base import BaseCommand

from ...models import Observation, Identification

header_observations = ['specimen_label', 'site_name', 'date_cest', 'method', 'repeat', 'sex', 'stage', 'id_confidence',
                       'suborder', 'family', 'genus', 'species']


def export_csv(file_path):
    with open(file_path, 'w') as file:
        headers = header_observations

        csv_writer = csv.DictWriter(file, headers)

        csv_writer.writeheader()

        observations = Observation.objects.all().order_by('specimen_label')

        for observation in observations:

            specimen = observation.specimen_label

            identifications = Identification.objects.filter(observation__specimen_label=specimen)

            for identification in identifications:
                if identification.confidence == Identification.Confidence.CONFIRMED:
                    selected_identification = identification
                else:
                    # TODO what should go here?

            # TODO check that the species / genus, sex and stage of the final identification is the same if there is more than one identification that was CONFIRMED

            row = {}

            row['specimen_label'] = observation.specimen_label
            row['site_name'] = observation.survey.visit.site.site_name
            row['date_cest'] = observation.survey.visit.date
            row['method'] = observation.survey.method
            row['repeat'] = observation.survey.repeat
            row['sex'] = identification.sex
            row['stage'] = identification.stage
            row['id_confidence'] = identification.confidence
            row['suborder'] = identification.suborder.suborder
            row['family'] = identification.family.family
            row['genus'] = identification.genus.genus
            row['species'] = identification.species.latin_name

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
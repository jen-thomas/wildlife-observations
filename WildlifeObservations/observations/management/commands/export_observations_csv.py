import argparse
import csv

from django.core.management.base import BaseCommand

from ...models import Observation, Identification
from ...utils import field_or_na

header_observations = ['specimen_label', 'site_name', 'date_cest', 'method', 'repeat', 'sex', 'stage', 'id_confidence',
                       'suborder', 'family', 'genus', 'species']


def export_csv(output_file):
    """
    Export data from a query into a CSV file which has a specified output file.

    Using an ORM query, get some data from the database and export specified fields into a CSV file which uses a set
    of headers.
    """

    headers = header_observations

    csv_writer = csv.DictWriter(output_file, headers)
    csv_writer.writeheader()

    observations = Observation.objects.all().order_by('specimen_label')

    for observation in observations:

        identifications = observation.identification_set.all() # get all identifications for this observation

        selected_identification = None

        for identification in identifications: # each observation may have many identifications with different certainties.
            if identification.confidence == Identification.Confidence.CONFIRMED: # select the confirmed identification only.
                selected_identification = identification
                break

        # TODO check that the species / genus, sex and stage of the final identification is the same if there is more than one identification that was CONFIRMED. Put this in a report.

        row = {}

        row['specimen_label'] = observation.specimen_label
        row['site_name'] = observation.survey.visit.site.site_name
        row['date_cest'] = observation.survey.visit.date
        row['method'] = observation.survey.method
        row['repeat'] = observation.survey.repeat
        row['sex'] = field_or_na(selected_identification, 'sex') # TODO add this to the following lines
        row['stage'] = identification.stage
        row['id_confidence'] = identification.confidence
        row['suborder'] = identification.suborder.suborder
        row['family'] = identification.family.family
        row['genus'] = identification.genus.genus
        row['species'] = identification.species.latin_name

        # TODO what should be done if one of the above fields is empty?

        csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        export_csv(options['output_file'])
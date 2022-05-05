import argparse
import csv

from django.core.management.base import BaseCommand

from ...models import Observation, Identification
from ...utils import field_or_empty_string

header_observations = ['specimen_label', 'site_name', 'date_cest', 'method', 'repeat', 'sex', 'stage', 'id_confidence',
                       'suborder', 'family', 'subfamily', 'genus', 'species']


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

        identifications = observation.identification_set.all()  # get all identifications for this observation

        selected_identification = None

        for identification in identifications:  # each observation may have many identifications with different certainties.
            if identification.confidence == Identification.Confidence.CONFIRMED:  # select the confirmed identification only.
                selected_identification = identification
                break

        # TODO check that the species / genus, sex and stage of the final identification is the same if there is more than one identification that was CONFIRMED. Put this in a report.

        row = {}

        row['specimen_label'] = observation.specimen_label
        row['site_name'] = observation.survey.visit.site.site_name
        row['date_cest'] = observation.survey.visit.date
        row['method'] = observation.survey.method
        row['repeat'] = observation.survey.repeat
        row['sex'] = selected_identification.sex  # shouldn't be null
        row['stage'] = selected_identification.stage  # shouldn't be null
        row['id_confidence'] = selected_identification.confidence  # shouldn't be null
        row['suborder'] = selected_identification.suborder.suborder  # shouldn't be null
        row['family'] = field_or_empty_string(selected_identification.family,
                                              'family')  # can be null if the identification cannot be determined to this taxonomic level
        row['subfamily'] = field_or_empty_string(selected_identification.subfamily,
                                                 'subfamily')  # can be null if the identification cannot be determined to this taxonomic level
        row['genus'] = field_or_empty_string(selected_identification.genus,
                                             'genus')  # can be null if the identification cannot be determined to this taxonomic level
        row['species'] = field_or_empty_string(selected_identification.species,
                                               'latin_name')  # can be null if the identification cannot be determined to this taxonomic level

        csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        export_csv(options['output_file'])

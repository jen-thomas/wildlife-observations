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

    If all observations have been identified, then the export of observations and identifications can consider just the
    finalised, confirmed identifications.
    - Where there are observations that have not been identified, these should be encountered in the data integrity
    checks.
    - Where there are observations that have an identification but the identification has not been confirmed, then
    these should also be encountered in the data integrity checks.
    - Where there is more than one confirmed identification for a particular observation, any conflicting differences
    in taxonomy should be encountered in the data integrity checks.
    - Where there is more than one confirmed identification for a particular observation, only one should be selected
    for the output.
    """

    headers = header_observations

    csv_writer = csv.DictWriter(output_file, headers)
    csv_writer.writeheader()

    confirmed_identifications = Identification.objects.filter(confidence=Identification.Confidence.CONFIRMED)

    selected_identification_specimen_label = set()

    for confirmed_identification in confirmed_identifications:
        if confirmed_identification.observation.specimen_label in selected_identification_specimen_label:
            break
        else:
            row = {}

            row['specimen_label'] = confirmed_identification.observation.specimen_label
            print(row['specimen_label'])
            row['site_name'] = confirmed_identification.observation.survey.visit.site.site_name
            row['date_cest'] = confirmed_identification.observation.survey.visit.date
            row['method'] = confirmed_identification.observation.survey.method
            row['repeat'] = confirmed_identification.observation.survey.repeat
            row['sex'] = confirmed_identification.sex  # shouldn't be null
            row['stage'] = confirmed_identification.stage  # shouldn't be null
            row['id_confidence'] = confirmed_identification.confidence  # shouldn't be null
            row['suborder'] = confirmed_identification.suborder.suborder  # shouldn't be null
            row['family'] = field_or_empty_string(confirmed_identification.family, 'family')  # can be null if the
            # identification cannot be determined to this taxonomic level
            row['subfamily'] = field_or_empty_string(confirmed_identification.subfamily, 'subfamily')  # can be null
            # if the identification cannot be determined to this taxonomic level
            row['genus'] = field_or_empty_string(confirmed_identification.genus, 'genus')  # can be null if the
            # identification cannot be determined to this taxonomic level
            row['species'] = field_or_empty_string(confirmed_identification.species, 'latin_name')  # can be null if the
            # identification cannot be determined to this taxonomic level

            csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        export_csv(options['output_file'])

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

    Finalised identifications are where an observation cannot be identified to one specific taxa. Therefore, there
    should be at least two finalised identifications for each observation in this case.

    This export will only deal with observations that have finalised (rather than confirmed) identifications.
    Observations that have both confirmed and finalised identifications should be spotted as part of the data integrity
    checks and therefore this case will not be dealt with in this export.

    All finalised identifications will be exported, therefore there should not be any finalised identifications if they
    are not still a possible identification.

    All identifications will be exported, not just one per observation in this case.
    """

    headers = header_observations

    csv_writer = csv.DictWriter(output_file, headers)
    csv_writer.writeheader()

    finalised_identifications = Identification.objects.filter(confidence=Identification.Confidence.FINALISED)

    # note that no deduplication of observations is done in this export because by the nature of these particular ones,
    # there will be more than one identification per observation that will be necessary.

    for finalised_identification in finalised_identifications:

        row = {}

        row['specimen_label'] = finalised_identification.observation.specimen_label
        row['site_name'] = finalised_identification.observation.survey.visit.site.site_name
        row['date_cest'] = finalised_identification.observation.survey.visit.date
        row['method'] = finalised_identification.observation.survey.method
        row['repeat'] = finalised_identification.observation.survey.repeat
        row['sex'] = finalised_identification.sex  # shouldn't be null
        row['stage'] = finalised_identification.stage  # shouldn't be null
        row['id_confidence'] = finalised_identification.confidence  # shouldn't be null
        row['suborder'] = finalised_identification.suborder.suborder  # shouldn't be null
        row['family'] = field_or_empty_string(finalised_identification.family, 'family')  # can be null if the
        # identification cannot be determined to this taxonomic level
        row['subfamily'] = field_or_empty_string(finalised_identification.subfamily, 'subfamily')  # can be null
        # if the identification cannot be determined to this taxonomic level
        row['genus'] = field_or_empty_string(finalised_identification.genus, 'genus')  # can be null if the
        # identification cannot be determined to this taxonomic level
        row['species'] = field_or_empty_string(finalised_identification.species, 'latin_name')  # can be null if the
        # identification cannot be determined to this taxonomic level

        csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')

    def handle(self, *args, **options):
        export_csv(options['output_file'])

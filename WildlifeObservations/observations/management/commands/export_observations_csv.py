import argparse
import csv

from django.core.management.base import BaseCommand

from ...models import Identification
from ...utils import field_or_empty_string

header_observations = ['specimen_label', 'site_name', 'date_cest', 'method', 'method_repeat', 'sex', 'stage',
                       'id_confidence', 'suborder', 'family', 'subfamily', 'genus', 'species']


def get_row_for_identification(identification):
    row = {}

    row['specimen_label'] = identification.observation.specimen_label
    print(row['specimen_label'])
    row['site_name'] = identification.observation.survey.visit.site.site_name
    row['date_cest'] = identification.observation.survey.visit.date
    row['method'] = identification.observation.survey.method
    row['method_repeat'] = identification.observation.survey.repeat
    row['sex'] = identification.sex  # shouldn't be null
    row['stage'] = identification.stage  # shouldn't be null
    row['id_confidence'] = identification.confidence  # shouldn't be null
    row['suborder'] = identification.suborder.suborder  # shouldn't be null
    row['family'] = field_or_empty_string(identification.family, 'family')  # can be null if the identification cannot
    # be determined to this taxonomic level
    row['subfamily'] = field_or_empty_string(identification.subfamily,
                                             'subfamily')  # can be null if the identification cannot be determined to
    # this taxonomic level
    row['genus'] = field_or_empty_string(identification.genus, 'genus')  # can be null if the identification cannot be
    # determined to this taxonomic level
    row['species'] = field_or_empty_string(identification.species,
                                           'latin_name')  # can be null if the identification cannot be determined to
    # this taxonomic level

    return row


def export_csv(output_file, practice_sites):
    """
    Export data from a query into a CSV file which has a specified output file.

    Using an ORM query, get some data from the database and export specified fields into a CSV file which uses a set
    of headers.

    If all observations have been identified, then the export of observations and identifications can consider just the
    confirmed and finalised identifications.
    - Observations should not have both confirmed and finalised identifications. These should be encountered
    in the data integrity checks.
    - Where there are observations that have not been identified, these should be encountered in the data integrity
    checks. These will not be exported.
    - Where there are observations that have an identification but the identification has not been confirmed or
    finalised, then these should also be encountered in the data integrity checks. These will not be exported.
    - Where there is more than one confirmed identification for a particular observation, only one should be selected
    for the output. Where there is more than one, the data integrity checks will ensure the confirmed identifications
    are for the same taxa.
    - Where an observation has finalised identifications, data integrity checks will ensure there are at least two.
    All finalised identifications for an observation will be exported.

    Observations from 'practice' sites, are excluded from the export. These were sites that were only visited once
    during the surveys and were not appropriate for visiting again.
    """

    headers = header_observations

    csv_writer = csv.DictWriter(output_file, headers)
    csv_writer.writeheader()

    # There must only be one identification exported for each observation, where the observation has a confirmed
    # identification. Note that this can be to any taxonomic level.

    confirmed_identifications = Identification.objects.exclude(
        observation__survey__visit__site__site_name__in=practice_sites).filter(
        confidence=Identification.Confidence.CONFIRMED)

    # Creating a set of the specimen labels ensures that only one confirmed identification for the same observation
    # should be exported. Data integrity checks will ensure that if there is more than one confirmed identification
    # for an observation, then it is for the same taxa. It is then also used as an extra check to make sure that no
    # finalised identifications can be exported if a confirmed identification for the same observation has been
    # exported. This case should be accounted for though in the data integrity checks.

    selected_identification_specimen_label = set()

    for confirmed_identification in confirmed_identifications:
        if confirmed_identification.observation.specimen_label not in selected_identification_specimen_label:
            row = get_row_for_identification(confirmed_identification)
            selected_identification_specimen_label.add(confirmed_identification.observation.specimen_label)

            csv_writer.writerow(row)
    print("Number of specimen labels after confirmed ids: ", len(selected_identification_specimen_label))

    # There could be more than one finalised identification that should be exported, so allow for more than one with
    # the same specimen label, but check that they are not in the set of observations that have confirmed
    # identifications.

    finalised_identifications = Identification.objects.exclude(
        observation__survey__visit__site__site_name__in=practice_sites).filter(
        confidence=Identification.Confidence.FINALISED)
    print("Number of finalised ids:", finalised_identifications.count())

    for finalised_identification in finalised_identifications:
        if finalised_identification.observation.specimen_label not in selected_identification_specimen_label:
            row = get_row_for_identification(finalised_identification)

            csv_writer.writerow(row)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')
        parser.add_argument('--practice_sites', type=str, nargs="*",
                            help='Site names of the practice sites to exclude from the export')

    def handle(self, *args, **options):
        export_csv(options['output_file'], options['practice_sites'])

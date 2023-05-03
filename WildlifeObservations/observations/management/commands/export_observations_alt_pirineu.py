import argparse
import csv

from django.core.management.base import BaseCommand

from . import export_observations_csv
from ...models import Identification
from ...utils import field_or_empty_string

header_observations = ['specimen_label', 'site_name', 'date_cest', 'sex', 'species']


def get_row_for_identification(identification):
    row = {}

    row['specimen_label'] = identification.observation.specimen_label
    row['site_name'] = identification.observation.survey.visit.site.site_name
    row['date_cest'] = identification.observation.survey.visit.date
    row['sex'] = identification.sex  # shouldn't be null
    row['species'] = field_or_empty_string(identification.species, 'latin_name')  # can be null if the identification
    # cannot be determined to this taxonomic level

    return row


def get_observations(practice_sites):

    selected_identification_specimen_label = set()
    selected_identifications = []

    confirmed_identifications = export_observations_csv.get_confirmed_observations(practice_sites)
                                                                                                                                                                                                                                                             
    for confirmed_identification in confirmed_identifications:
        if confirmed_identification.observation.specimen_label not in selected_identification_specimen_label:
            row = get_row_for_identification(confirmed_identification)
            selected_identification_specimen_label.add(confirmed_identification.observation.specimen_label)
            selected_identifications.append(row)

    print("Number of specimen labels after confirmed ids: ", len(selected_identification_specimen_label))

    # do not include finalised identifications because these are not definitive
    # finalised_identifications = export_observations_csv.get_finalised_observations(practice_sites)
    #
    # print("Number of finalised ids:", finalised_identifications.count())
    #
    # for finalised_identification in finalised_identifications:
    #     if finalised_identification.observation.specimen_label not in selected_identification_specimen_label:
    #         row = get_row_for_identification(finalised_identification)
    #         selected_identifications.append(row)

    print("Number of selected identifications:", len(selected_identifications))

    return selected_identifications


def export_csv(output_file, identifications):

    headers = header_observations

    csv_writer = csv.DictWriter(output_file, headers)
    csv_writer.writeheader()

    for identification in identifications:
        csv_writer.writerow(identification)
        print(identification)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=argparse.FileType('w'), help='Path to the file or - for stdout')
        parser.add_argument('--practice_sites', type=str, nargs="*",
                            help='Site names of the practice sites to exclude from the export')

    def handle(self, *args, **options):
        selected_identifications = get_observations(options['practice_sites'])
        export_csv(options['output_file'], selected_identifications)



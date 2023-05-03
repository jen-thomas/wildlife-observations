import argparse
import csv

from django.core.management.base import BaseCommand

from . import export_observations_csv
from ...models import Identification
from ...utils import field_or_empty_string

header_observations = ['specimen_label', 'site_name', 'date_cest', 'sex', 'species']


def get_row_for_identification(identification):
    """
    Get the attributes of each identification.

    Return a dictionary.
    """

    row = {}

    row['specimen_label'] = identification.observation.specimen_label
    row['site_name'] = identification.observation.survey.visit.site.site_name
    row['date_cest'] = identification.observation.survey.visit.date
    row['sex'] = identification.sex  # shouldn't be null
    row['species'] = field_or_empty_string(identification.species, 'latin_name')  # can be null if the identification
    # cannot be determined to this taxonomic level, but these should be removed by the filter

    return row


def get_identifications_to_species(identifications):
    """
    Exclude all identifications where the species is null.

    Return a queryset of the identifications where species is not null.
    """

    ids_species = identifications.exclude(species__isnull=True)

    return ids_species


def get_observations(practice_sites):
    """
    Get all observations for each of the sites, excluding those found at the practice sites.

    Conditions applied to the observations obtained are:
    - species is not null
    - identification is confirmed

    Return list of confirmed identifications.
    """

    selected_identifications = []

    confirmed_identifications = export_observations_csv.get_confirmed_observations(practice_sites)
    confirmed_ids_species = get_identifications_to_species(confirmed_identifications)

    for confirmed_identification in confirmed_ids_species:
        row = get_row_for_identification(confirmed_identification)
        selected_identifications.append(row)

    print("Number of selected identifications:", len(selected_identifications))

    return selected_identifications


def export_csv(output_file, identifications):
    """
    Export a CSV of the chosen identifications.

    Output the CSV file.
    """

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
import argparse
import csv

from pyproj import Transformer
from django.core.management.base import BaseCommand
from django.db.models import Count

from . import export_observations_csv

header_observations = ['species', 'date_cest', 'x', 'y', 'altitude', 'site_name', 'count', 'sex']


def convert_latlon_to_utm(latitude, longitude):

    # Create a transformer
    transformer = Transformer.from_crs("epsg:4326", "epsg:32631")

    # Use the transform function to convert
    easting, northing = transformer.transform(latitude, longitude)

    return easting, northing


def get_row_for_identification(identification):
    """
    Get the attributes of each identification.

    Return a dictionary.
    """

    row = {}

    # Convert lat lon to UTM coordinates
    latitude = identification['observation__survey__visit__site__latitude_start']\
                      + ((identification['observation__survey__visit__site__latitude_end']
                          - identification['observation__survey__visit__site__latitude_start']) / 2)
    longitude = identification['observation__survey__visit__site__longitude_start']\
                      + ((identification['observation__survey__visit__site__longitude_end']
                          - identification['observation__survey__visit__site__longitude_start']) / 2)

    coords = convert_latlon_to_utm(latitude, longitude)

    row['x'] = '{:06.0f}'.format(coords[0])
    row['y'] = '{:07.0f}'.format(coords[1])

    # Convert male and female into the codes required for Alt Pirineu form
    if identification['sex'] == "Female":
        row['sex'] = 2
    elif identification['sex'] == "Male":
        row['sex'] = 1
    else:
        row['sex'] = 0

    row['site_name'] = identification['observation__survey__visit__site__site_name']
    row['altitude'] = '{:.0f}'.format(identification['observation__survey__visit__site__altitude_start']\
                      + ((identification['observation__survey__visit__site__altitude_end']
                          - identification['observation__survey__visit__site__altitude_start']) / 2))
    row['date_cest'] = identification['observation__survey__visit__date']
    row['species'] = identification['species__latin_name']
    row['count'] = identification['count']

    return row


def get_identifications_to_species(identifications):
    """
    Exclude all identifications where the species is null.

    Return a queryset of the identifications where species is not null.
    """

    ids_species = identifications.exclude(species__isnull=True)

    return ids_species


def summarise_observations(identifications):
    """
    Summarise the observations by species, date, site, age and sex, then count the number of each records within each
    of these groups.

    Return a queryset of the summarised data.
    """

    ids_summarised = identifications.values('observation__survey__visit__site__site_name',
                                            'observation__survey__visit__site__latitude_start',
                                            'observation__survey__visit__site__latitude_end',
                                            'observation__survey__visit__site__longitude_start',
                                            'observation__survey__visit__site__longitude_end',
                                            'observation__survey__visit__site__altitude_start',
                                            'observation__survey__visit__site__altitude_end',
                                            'observation__survey__visit__date', 'species__latin_name', 'sex')\
        .annotate(count = Count('species'))

    return ids_summarised


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
    summarised_ids = summarise_observations(confirmed_ids_species)

    for summarised_id in summarised_ids:
        row = get_row_for_identification(summarised_id)
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
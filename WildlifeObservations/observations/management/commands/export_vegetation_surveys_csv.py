import csv

from django.core.management.base import BaseCommand

from ...models import VegetationStructure, Plot

header_vegetation_survey = ['site_name', 'date_cest', 'plot_distance_from_start_m', 'percentage_vegetation_cover',
                            'percentage_bare_ground', 'percentage_rock', 'height_75percent', 'max_height',
                            'density_01', 'density_02', 'density_03', 'density_04', 'density_05']


def export_csv(file_path):
    """
    Export data from a query into a CSV file which has a specified path and filename.

    Using an ORM query, get some data from the database and export specified fields into a CSV file which uses a set
    of headers.
    """

    with open(file_path, 'w') as file:
        headers = header_vegetation_survey

        csv_writer = csv.DictWriter(file, headers)
        csv_writer.writeheader()

        vegetation_surveys = VegetationStructure.objects.all()

        for vegetation_survey in vegetation_surveys:

            plot = Plot.objects.get(plot=Plot)
            row = {}

            row['site_name'] = plot.visit.site.site_name
            row['date_cest'] = plot.visit.date
            row['plot_distance_from_start_m'] = plot.position
            row['percentage_vegetation_cover'] = vegetation_survey.percentage_vegetation_cover
            row['percentage_bare_ground'] = vegetation_survey.percentage_bare_ground
            row['percentage_rock'] = vegetation_survey.percentage_rock
            row['height_75percent'] = vegetation_survey.height_75percent
            row['max_height'] = vegetation_survey.max_height
            row['density_01'] = vegetation_survey.density_01
            row['density_02'] = vegetation_survey.density_02
            row['density_03'] = vegetation_survey.density_03
            row['density_04'] = vegetation_survey.density_04
            row['density_05'] = vegetation_survey.density_05

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
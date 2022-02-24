from django.core.management.base import BaseCommand

from ...reports import SpeciesReport


class Command(BaseCommand):
    help = 'Print reports'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        species_reports = SpeciesReport()

        print("---------- Number of observations ----------")
        print("Total:", species_reports.observations_count())

        for row in species_reports.observations_suborder_count():
            print(row["suborder"], row["count"])

        print("\n---------- Number of individual observations identified ----------")
        print(species_reports.identified_observations_count())

        print("\n---------- Number of each species identified ----------")
        for row in species_reports.species_identified_count():
            print(row["species_name"], row["count"])


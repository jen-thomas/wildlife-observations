from django.core.management.base import BaseCommand

from ...reports import SpeciesReport


class Command(BaseCommand):
    help = 'Print reports'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        species_reports = SpeciesReport()

        for row in species_reports.species_identified_count():
            print(row["species_name"], row["count"])

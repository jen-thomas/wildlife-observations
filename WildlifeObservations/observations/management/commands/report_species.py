from django.core.management.base import BaseCommand

from ...reports import SpeciesReport


class Command(BaseCommand):
    help = 'Print reports about species'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        species_reports = SpeciesReport()

        print("\n---------- Number of each species identified ----------")

        number_confirmed_species = species_reports.number_confirmed_species_observed()
        print("\nTotal number of confirmed species observed: ", number_confirmed_species)

        number_unconfirmed_species = len(species_reports.unconfirmed_species_observed())
        print("Total number of unconfirmed species observed: ", number_unconfirmed_species)

        for row in species_reports.species_identified_count():
            print(row["species_name"], row["count"])

        print("\n-Unconfirmed species-")
        # TODO - remove the confirmed species from this list
        for species in species_reports.unconfirmed_species_observed():
            print(species)

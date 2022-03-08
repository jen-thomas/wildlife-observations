from django.core.management.base import BaseCommand

from ...reports import SpeciesReport, VisitReport


class Command(BaseCommand):
    help = 'Print reports'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        species_reports = SpeciesReport()
        visit_reports = VisitReport()

        print("---------- Number of observations ----------")
        print("Total:", species_reports.observations_count())

        for row in species_reports.observations_suborder_count():
            print(row["suborder"], row["count"])

        print("\n---------- Number of individual observations identified ----------")
        print(species_reports.identified_observations_count())

        done = (species_reports.identified_observations_count()/species_reports.observations_count())*100
        to_do = 100-done

        print("Done:", done, "%")
        print("To do:", to_do, "%")

        print("\n---------- Number of each species identified ----------")
        for row in species_reports.species_identified_count():
            print(row["species_name"], row["count"])

        number_confirmed_species = species_reports.number_confirmed_species_observed()
        print("Total number of confirmed species observed: ", number_confirmed_species)

        number_unconfirmed_species = species_reports.number_unconfirmed_species_observed()
        print("Total number of unconfirmed species observed: ", number_unconfirmed_species)

        print("\n------------ Sites visited ------------")

        print("\nTotal number of sites in each area.")


        print("\nTotal number of visits to each site.")
        for row in visit_reports.summarise_visits():
            print(row['site_name'], row["count"])

        print("\nSummary of suborders observed during each survey.")
        for row in visit_reports.summarise_suborder_survey():
            print(row['survey'], 'Caelifera:', row['Caelifera'], 'Ensifera:', row['Ensifera'], 'Unknown:', row['observations_not_identified'])


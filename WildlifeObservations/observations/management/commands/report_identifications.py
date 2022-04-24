from django.core.management.base import BaseCommand

from ...reports import SpeciesReport


class Command(BaseCommand):
    help = 'Print reports about observations and identifications'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        species_reports = SpeciesReport()

        print("---------- Observations ----------")

        counting_observations = species_reports.observations_count()

        print("Total number of observations:", counting_observations)

        counting_suborders = species_reports.observations_suborder_count()

        print("Caelifera:", len(counting_suborders['Caelifera']), ",",
              100 * (len(counting_suborders['Caelifera']) / counting_observations).__round__(3), "%")
        print("Ensifera:", len(counting_suborders['Ensifera']), ",",
              100 * (len(counting_suborders['Ensifera']) / counting_observations).__round__(3), "%")
        print("Number of observations without an identification:",
              counting_observations - len(counting_suborders['Caelifera']) - len(counting_suborders['Ensifera']) - len(counting_suborders['todo']))
        print("Number of identifications without a suborder:", len(counting_suborders['todo']))

        print("\n---------- Observations identified ----------")

        done = (species_reports.identified_observations_count() / species_reports.observations_count()) * 100
        to_do = 100 - done

        print("Total number of observations identified:", species_reports.identified_observations_count())
        print("Done:", done, "%")
        print("To do:", to_do, "%")

        print("\nTotal number of observations with finalised identifications:",
              species_reports.identified_observations_finalised_count())

        print("\nNumber of unique observations identified to species:",
              species_reports.identified_observations_to_species_count())
        print("Number of unique observations identified to genus:",
              species_reports.identified_observations_to_genus_count())
        print("Number of observations only identified to genus:",
              species_reports.identified_observations_to_genus_not_species_count())

        print("\n---------- Number of each stage identified ----------")

        print("\nStages identified:")
        for identification in species_reports.identifications_stage_count():
            print(identification["stage"], identification["count"])

        print("\nStage with confidence:")
        for identification in species_reports.identifications_stage_confidence_count():
            if identification["stage"] == "Adult":
                print(identification["stage"], identification["confidence"], identification["count"])
            elif identification["stage"] == "Nymph":
                print(identification["stage"], identification["confidence"], identification["count"])

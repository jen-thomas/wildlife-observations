from django.core.management.base import BaseCommand

from ...reports import SpeciesReport


class Command(BaseCommand):
    help = 'Print reports about observations and identifications'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        species_reports = SpeciesReport()

        print("---------- Number of observations ----------")
        print("Total:", species_reports.observations_count())

        for row in species_reports.observations_suborder_count():
            print("\n", row["suborder"], row["count"], (100*row["count"]/species_reports.observations_count()).__round__(1), "%")

        print("\n---------- Observations identified ----------")

        done = (species_reports.identified_observations_count()/species_reports.observations_count())*100
        to_do = 100-done

        print("Total number of observations identified:", species_reports.identified_observations_count())
        print("Done:", done, "%")
        print("To do:", to_do, "%")

        print("\nNumber of unique observations identified to species:", species_reports.identified_observations_to_species_count())
        print("Number of unique observations identified to genus:", species_reports.identified_observations_to_genus_count())
        print("Number of observations only identified to genus:", species_reports.identified_observations_to_genus_not_species_count())

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
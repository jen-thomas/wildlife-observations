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

        print("Caelifera:", len(counting_suborders['Caelifera']), "=",
              100 * (len(counting_suborders['Caelifera']) / counting_observations).__round__(3), "%")
        print("Ensifera:", len(counting_suborders['Ensifera']), "=",
              100 * (len(counting_suborders['Ensifera']) / counting_observations).__round__(3), "%")
        print("Number of observations without an identification:",
              counting_observations - len(counting_suborders['Caelifera']) - len(counting_suborders['Ensifera']) - len(counting_suborders['todo']))

        print("\n---------- Observations identified ----------")

        print("\nTotal number of observations with finalised identifications (yes, confirmed, cannot identify further, small nymphs hard to ID):",
              species_reports.identified_observations_finalised_count())

        counting_species_identified_finalised = species_reports.identified_observations_to_species_finalised()
        counting_species_identified_todo = species_reports.identified_observations_to_species_todo()

        print("\nNumber of unique observations identified to species, identification CONFIRMED:", len(counting_species_identified_finalised['Confirmed']))
        print("\nNumber of unique observations identified to species, identification to REVIEW:", len(counting_species_identified_todo['Review']))
        print("Number of unique observations identified to species, identification to CHECK AFTER MUSEUM:", len(counting_species_identified_todo['CheckMuseum']))
        print("Number of unique observations identified to species, identification to CHECK:", len(counting_species_identified_todo['Check']))
        print("Number of unique observations identified to species, identification to REDO / IN PROGRESS:", len(counting_species_identified_todo['Redo']) + len(counting_species_identified_todo['InProgress']))

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

        print("\n-----THINGS TO CHECK-----")

        print("\n-Number of identifications without a suborder:", len(counting_suborders['todo']), ":", counting_suborders['todo'])
        print("\n-Number of observations identified to species which have been marked as cannot be ID'd further:", len(counting_species_identified_finalised['CannotIDfurther']), ":", counting_species_identified_finalised['CannotIDfurther'])

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

        print("Total number of observations:", len(counting_observations))

        counting_suborders = species_reports.observations_suborder()

        print("Caelifera:", len(counting_suborders['Caelifera']), "=",
              100 * (len(counting_suborders['Caelifera']) / len(counting_observations)).__round__(3), "%")
        print("Ensifera:", len(counting_suborders['Ensifera']), "=",
              100 * (len(counting_suborders['Ensifera']) / len(counting_observations)).__round__(3), "%")
        print("Number of observations without an identification:",
              len(counting_observations) - len(counting_suborders['Caelifera']) - len(
                  counting_suborders['Ensifera']) - len(counting_suborders['todo']))

        print("\n---------- Observations identified ----------")

        print(
            "\nTotal number of observations with finalised identifications (yes, confirmed, cannot identify further, "
            "small nymphs hard to ID):",
            species_reports.identified_observations_finalised_count())

        counting_species_identified = species_reports.identified_observations_to_species()

        total_identifications_species_unique = species_reports.unique_observations_identified_to_species(counting_species_identified)

        print("Total number of observations identified to species:", len(total_identifications_species_unique))
        print("\nNumber of unique observations identified to species, identification CONFIRMED:",
              len(counting_species_identified['Confirmed']))
        print("Number of unique observations identified to species, identification to REVIEW:",
              len(counting_species_identified['Review']))
        print("Number of unique observations identified to species, identification to CHECK AFTER MUSEUM:",
              len(counting_species_identified['CheckMuseum']))
        print("Number of unique observations identified to species, identification to CHECK:",
              len(counting_species_identified['Check']))
        print("Number of unique observations identified to species, identification to REDO / IN PROGRESS:",
              len(counting_species_identified['Redo']))
        print("Number of unique observations identified to species, identification CANNOT ID FURTHER:",
              len(counting_species_identified['CannotIDfurther']))
        print("Number of unique observations identified to species, identification NYMPHS HARD TO ID:",
              len(counting_species_identified['NymphsIDhard']))
        print("Number of unique observations identified to species, identification IN PROGRESS:",
              len(counting_species_identified['InProgress']))
        print("Number of unique observations identified to species, identification MISSING CONFIRMATION:",
              len(counting_species_identified['NoConfirmation']))

        counting_genus_identified = species_reports.identified_observations_to_genus_not_species()

        print("\nNumber of unique observations only identified to genus:", counting_genus_identified['Total'])
        print("\nNumber of unique observations only identified to genus, identification CONFIRMED:",
              len(counting_genus_identified['Confirmed']))
        print("Number of unique observations only identified to genus, identification to REVIEW:",
              len(counting_genus_identified['Review']))
        print("Number of unique observations only identified to genus, identification CANNOT ID FURTHER:",
              len(counting_genus_identified['CannotIDfurther']))
        print("Number of unique observations only identified to genus, identification NYMPHS HARD TO ID:",
              len(counting_genus_identified['NymphsIDhard']))
        print("Number of unique observations only identified to genus, identification to CHECK AFTER MUSEUM:",
              len(counting_genus_identified['CheckMuseum']))
        print("Number of unique observations only identified to genus, identification to CHECK:",
              len(counting_genus_identified['Check']))
        print("Number of unique observations only identified to genus, identification to REDO:",
              len(counting_genus_identified['Redo']))
        print("Number of unique observations only identified to genus, identification IN PROGRESS:",
              len(counting_genus_identified['InProgress']))
        print("Number of unique observations only identified to genus, identification NO CONFIRMATION:",
              len(counting_genus_identified['NoConfirmation']))

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

        print("\n-Number of observations without an identification:",
              len(counting_observations) - len(counting_suborders['Caelifera']) - len(
                  counting_suborders['Ensifera']) - len(counting_suborders['todo']), ":",
              counting_observations - counting_suborders['Caelifera'] - counting_suborders['Ensifera'] -
              counting_suborders['todo'])
        print("\n-Number of identifications without a suborder:", len(counting_suborders['todo']), ":",
              counting_suborders['todo'])
        print("\n-Number of observations identified to species which have been marked as cannot be ID'd further:",
              len(counting_species_identified['CannotIDfurther']), ":", counting_species_identified['CannotIDfurther'])

        print("\n-ID'd to species to REVIEW:", len(counting_species_identified['Review']), ":",
              counting_species_identified['Review'])
from django.core.management.base import BaseCommand

from ...data_integrity_checks import IdentificationDataChecks


class Command(BaseCommand):
    help = 'Check identification data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        identification_checks = IdentificationDataChecks()

        practice_sites = ["TAV02", "TAV04", "MOL07", "MOL10", "BOR01"]

        print("***** Identifications without a sex (adults only) *****")
        print(len(identification_checks.check_identification_has_sex_adults_only()), "results:\n")
        for identification in identification_checks.check_identification_has_sex_adults_only():
            print(identification['specimen_label'])

        print("\n***** Identifications without a sex (all stages) *****")
        print(len(identification_checks.check_identification_has_sex()), "results:\n")
        for identification in identification_checks.check_identification_has_sex():
            print(identification['specimen_label'])

        print("\n***** Identifications without a stage *****")
        print(len(identification_checks.check_identification_has_stage()), "results:\n")
        for identification in identification_checks.check_identification_has_stage():
            print(identification['specimen_label'])

        print("\n***** Identifications without a confidence *****")
        print(len(identification_checks.check_identification_has_confidence(practice_sites)), "results:\n")
        for identification in identification_checks.check_identification_has_confidence(practice_sites):
            print(identification['specimen_label'])

        print("\n***** Observations without an identification *****")
        print(len(identification_checks.find_observations_without_identification()), "results:\n")
        for observation in identification_checks.find_observations_without_identification():
            print(observation)

        print("\n***** Observations without a confirmed or finalised identification *****")
        observations_without_confirmation_or_finalisation = identification_checks.find_observations_without_confirmed_or_finalised_identification()
        print(len(observations_without_confirmation_or_finalisation), "results:\n")
        for observation in observations_without_confirmation_or_finalisation:
            print(observation)

        print("\n***** Observations without a confirmed or finalised identification (adults only) *****")
        print(len(identification_checks.get_unconfirmed_unfinalised_adults(observations_without_confirmation_or_finalisation)),
              "results:\n")
        for observation in identification_checks.get_unconfirmed_unfinalised_adults(observations_without_confirmation_or_finalisation):
            print(observation)

        print("\n***** Finalised/confirmed identifications with different sexes *****")
        print(len(identification_checks.check_finalised_confirmed_identifications_sex()), "results:\n")
        for identification in identification_checks.check_finalised_confirmed_identifications_sex():
            print(identification)

        print("\n***** Finalised/confirmed identifications with different stages *****")
        print(len(identification_checks.check_finalised_confirmed_identifications_stage()), "results:\n")
        for identification in identification_checks.check_finalised_confirmed_identifications_stage():
            print(identification)

        print("\n***** Confirmed identifications with different taxonomy *****")
        print(len(identification_checks.check_confirmed_identifications_taxonomy()), "results:\n")
        for identification in identification_checks.check_confirmed_identifications_taxonomy():
            print(identification)

        print("\n***** Observations with confirmed and finalised identifications *****")
        print(len(identification_checks.observations_with_confirmed_and_finalised_identifications()), "results:\n")
        for identification in identification_checks.observations_with_confirmed_and_finalised_identifications():
            print(identification)
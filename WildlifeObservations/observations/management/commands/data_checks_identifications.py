from django.core.management.base import BaseCommand

from ...data_integrity_checks import IdentificationDataChecks


class Command(BaseCommand):
    help = 'Check identification data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        identification_checks = IdentificationDataChecks()

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
        print(len(identification_checks.check_identification_has_confidence()), "results:\n")
        for identification in identification_checks.check_identification_has_confidence():
            print(identification['specimen_label'])

        print("\n***** Observations without an identification *****")
        print(len(identification_checks.find_observations_without_identification()), "results:\n")
        for observation in identification_checks.find_observations_without_identification():
            print(observation)

        print("\n***** Observations without a confirmed or finalised identification *****")
        print(len(identification_checks.find_observations_without_confirmed_or_finalised_identification()), "results:\n")
        for observation in identification_checks.find_observations_without_confirmed_or_finalised_identification():
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
from django.core.management.base import BaseCommand

from ...data_integrity_checks import IdentificationDataChecks


class Command(BaseCommand):
    help = 'Check identification data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        identification_checks = IdentificationDataChecks()

        print("***** Identifications without a sex (all stages) *****")
        print(len(identification_checks.check_identification_has_sex()), "results:\n")
        for identification in identification_checks.check_identification_has_sex():
            print(identification['specimen_label'])

        print("\n***** Identifications without a stage *****")
        print(len(identification_checks.check_identification_has_stage()), "results:\n")
        for identification in identification_checks.check_identification_has_stage():
            print(identification['specimen_label'])
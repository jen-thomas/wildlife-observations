from django.core.management.base import BaseCommand

from ...data_integrity_checks import ObservationDataChecks


class Command(BaseCommand):
    help = 'Check observation data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        observation_checks = ObservationDataChecks()

        print("***** Observations without a suborder *****")
#        print(len(observation_checks.find_observations_without_suborder()), "results:\n")
        for observation in observation_checks.find_observations_without_suborder():
            print(observation)

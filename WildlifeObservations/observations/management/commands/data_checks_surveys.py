from django.core.management.base import BaseCommand

from ...data_integrity_checks import SurveyDataChecks


class Command(BaseCommand):
    help = 'Check survey data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        survey_checks = SurveyDataChecks()

        print("***** Surveys without met data *****")
        print(len(survey_checks.find_surveys_without_met_conditions()), "results:\n")
        for surveys_without_met_conditions in survey_checks.find_surveys_without_met_conditions():
            print(surveys_without_met_conditions)

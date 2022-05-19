import datetime

from django.core.management.base import BaseCommand

from ...reports import SurveyReport


class Command(BaseCommand):
    help = 'Print summary reports about a specified survey'

    def add_arguments(self, parser):
        parser.add_argument('site_name', type=str,
                            help="Site name")
        parser.add_argument('date', type=datetime.date.fromisoformat, help='Date of survey')
        parser.add_argument('method', type=str, help='Survey method')
        parser.add_argument('repeat', type=int, help='Survey method repeat')

    def handle(self, *args, **options):
        survey_reports = SurveyReport()

        survey = survey_reports.get_survey_object(options['site_name'], options['date'], options['method'], options['repeat'])

        print("\nSummary of suborders observed during this survey (confirmed and finalised identifications only):", survey)
        for suborder, observations in survey_reports.summarise_survey_suborder(survey).items():
            print(suborder, len(observations))

        print("\nSummary of confirmed or finalised taxa during this survey:", survey)
        for taxa, count in survey_reports.summarise_survey_confirmed_finalised_taxa(survey):
            print(taxa, count)

        print("\nList of observations for this survey:", survey)
        print("Total:", len(survey_reports.list_survey_observations(survey)))
        for row in survey_reports.list_survey_observations(survey):
            print(row)

        print("\nList of identifications for this survey:", survey)
        print("Total:", len(survey_reports.list_survey_identifications(survey)))
        for row in survey_reports.list_survey_identifications(survey):
            print(row)


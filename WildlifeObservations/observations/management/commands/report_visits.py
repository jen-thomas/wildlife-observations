from django.core.management.base import BaseCommand

from ...reports import VisitReport


class Command(BaseCommand):
    help = 'Print reports about visits and sites'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        visit_reports = VisitReport()

        print("\n------------ Sites visited ------------")

        print("\nTotal number of sites in each area.")
        for row in visit_reports.summarise_sites():
            print(row['area'], row['count'])

        print("\nTotal number of visits to each site.")
        for row in visit_reports.summarise_visits():
            print(row['site_name'], row["count"])

        # print("\nSummary of observations from each survey.")
        # for row in visit_reports.summarise_survey():
        #     print(row['survey'], ":", row['count'])

        print("\nSummary of suborders observed during each survey.")
        for row in visit_reports.summarise_suborder_survey():
            print(row['survey'], 'Caelifera:', row['Caelifera'], 'Ensifera:', row['Ensifera'], 'Unknown:', row['observations_not_identified'])


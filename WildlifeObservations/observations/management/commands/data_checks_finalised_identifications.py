from django.core.management.base import BaseCommand

from ...data_integrity_checks import IdentificationDataChecks


class Command(BaseCommand):
    help = 'Check finalised identification data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        identification_checks = IdentificationDataChecks()
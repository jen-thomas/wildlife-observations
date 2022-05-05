from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Identification

class Command(BaseCommand):
    help = 'Updates confidence reason field in database.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.confidence_yes_to_confirmed()

    def confidence_yes_to_confirmed(self):
        identifications = Identification.objects.filter(confidence=Identification.Confidence.YES).update(confidence=Identification.Confidence.CONFIRMED)
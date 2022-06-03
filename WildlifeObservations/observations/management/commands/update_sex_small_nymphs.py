from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Identification


def get_small_nymph_no_sex_identifications():
    """Get the identifications of nymphs that have been marked as being confirmed because they are too small to identify
     further.

     Return the queryset of objects.
     """

    rows_to_update = Identification.objects.filter(stage=Identification.Stage.NYMPH).filter(
        confidence_reason=Identification.ConfidenceReason.SMALL_NYMPH_HARD_TO_ID).filter(sex__isnull=True)

    return rows_to_update


def update_sex_unknown_small_nymphs():
    """Update the objects with unknown sex."""

    rows_to_update = get_small_nymph_no_sex_identifications()

    rows_to_update.update(sex=Identification.Sex.UNKNOWN)


class Command(BaseCommand):
    help = 'Updates identifications of small nymphs that do not currently have a sex defined.'

    @transaction.atomic
    def handle(self, *args, **options):
        update_sex_unknown_small_nymphs()

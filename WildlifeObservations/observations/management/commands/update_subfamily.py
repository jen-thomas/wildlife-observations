from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F

from ...models import Identification, TaxonomyGenus


def get_identifications_without_subfamily_with_genus():
    """
    Get the identifications that have a genus but no subfamily. Return a queryset.
    """

    return Identification.objects.filter(genus__isnull=False).filter(subfamily__isnull=True)


def update_subfamily():
    """
    Add the subfamily where it is null. Get the subfamily from the genus that is in the identification. Only update the
    identifications that have a genus and a blank subfamily.
    """

    identifications_to_update = get_identifications_without_subfamily_with_genus()

    for identification in identifications_to_update:
        identification_subfamily = TaxonomyGenus.objects.get(genus=identification.genus).subfamily
        identification.subfamily = identification_subfamily
        identification.subfamily.save()
        print("Updating ", identification.observation.specimen_label, "with ", identification_subfamily)


class Command(BaseCommand):
    help = 'Updates subfamily according to genus of identification.'

    @transaction.atomic
    def handle(self, *args, **options):

        update_subfamily()

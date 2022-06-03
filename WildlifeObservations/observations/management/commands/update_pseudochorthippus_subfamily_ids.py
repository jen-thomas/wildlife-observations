from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from ...models import Identification, TaxonomySubfamily, TaxonomyGenus


def get_subfamily_for_genus(genus):
    """Get the subfamily for a particular genus.

    Return the subfamily object."""

    subfamily = TaxonomySubfamily.objects.get(taxonomygenus__genus=genus)

    return subfamily


def pseudochorthippus_to_gomphocerinae():
    """Update the identifications in the database to correct the subfamily for the genus Pseudochorthippus."""

    genus = TaxonomyGenus.objects.get(genus="Pseudochorthippus")
    subfamily = get_subfamily_for_genus(genus)
    get_identifications_pseudochorthippus_incorrect_subfamily(genus).update(subfamily=subfamily)


def get_identifications_pseudochorthippus_incorrect_subfamily(genus):
    """Get the identifications which have a particular genus and subfamily."""

    incorrect_subfamily = TaxonomySubfamily.objects.get(subfamily="Oedipodinae")
    rows_to_update = Identification.objects.filter(Q(Q(genus=genus) & Q(subfamily=incorrect_subfamily)))

    return rows_to_update


class Command(BaseCommand):
    help = 'Updates subfamily of identifications of Pseudochorthippus in database which was incorrect.'

    @transaction.atomic
    def handle(self, *args, **options):
        pseudochorthippus_to_gomphocerinae()

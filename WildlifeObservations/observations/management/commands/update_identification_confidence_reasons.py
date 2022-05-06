from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Identification


# Some lines in this command have been commented out because they were used with choices in the models which have now
# been deprecated. They have been left here in this state in case they are needed for future reference.

# def confidence_yes_to_confirmed():
#     get_identifications_with_confidence_without_reasons(Identification.Confidence.YES).update(
#         confidence=Identification.Confidence.CONFIRMED)


def confirmed_add_reason():
    get_identifications_with_confidence_without_reasons(Identification.Confidence.CONFIRMED).update(
        confidence_reason=Identification.ConfidenceReason.ID_CERTAIN)


def check_add_reason():
    get_identifications_with_confidence_without_reasons(Identification.Confidence.CHECK).update(
        confidence_reason=Identification.ConfidenceReason.ID_NEEDS_CONFIRMATION)


def check_museum_add_reason():
    get_identifications_with_confidence_without_reasons(Identification.Confidence.CHECK_IN_MUSEUM).update(
        confidence_reason=Identification.ConfidenceReason.ID_NEEDS_CONFIRMATION)


def review_add_reason():
    get_identifications_with_confidence_without_reasons(Identification.Confidence.REVIEW).update(
        confidence_reason=Identification.ConfidenceReason.ID_UNCERTAIN)


def redo_add_reason():
    get_identifications_with_confidence_without_reasons(Identification.Confidence.REDO).update(
        confidence_reason=Identification.ConfidenceReason.ID_INCORRECT)


def inprogress_add_reason():
    get_identifications_with_confidence_without_reasons(Identification.Confidence.IN_PROGRESS).update(
        confidence_reason=Identification.ConfidenceReason.ID_INCOMPLETE)


# def confidence_nymph_to_reason():
#     get_identifications_with_confidence_without_reasons(Identification.Confidence.SMALL_NYMPH_HARD_TO_ID).update(
#         confidence=Identification.Confidence.CONFIRMED,
#         confidence_reason=Identification.ConfidenceReason.SMALL_NYMPH_HARD_TO_ID)
#
#
# def confidence_cannot_det_to_reason():
#     get_identifications_with_confidence_without_reasons(Identification.Confidence.CANNOT_DETERMINE_FURTHER).update(
#         confidence=Identification.Confidence.CONFIRMED,
#         confidence_reason=Identification.Confidence.CANNOT_DETERMINE_FURTHER)


def get_identifications_with_confidence_without_reasons(confidence):
    return Identification.objects.filter(confidence=confidence).filter(confidence_reason__isnull=True)


class Command(BaseCommand):
    help = 'Updates confidence and confidence reason fields in database.'

    @transaction.atomic
    def handle(self, *args, **options):
        # confidence_yes_to_confirmed()
        confirmed_add_reason()
        check_add_reason()
        check_museum_add_reason()
        review_add_reason()
        redo_add_reason()
        inprogress_add_reason()
        # confidence_nymph_to_reason()
        # confidence_cannot_det_to_reason()
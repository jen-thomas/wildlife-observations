from django.db.models import Count

from .models import Identification, Observation


class SpeciesReport:
    def __init__(self):
        pass

    def species_identified_count(self):
        """Returns list of dictionaries with species name and count

        For example:
        [{'species_name': 'Mallard', 'count': 5},
         {'species_name': 'Horse', 'count': 6},
         ]
        """

        qs = Identification.objects.filter(species__isnull=False).values("species__latin_name").annotate(total=Count("species")).order_by("-total")

        result = []

        for identification in qs:
            result.append({"species_name": identification["species__latin_name"], "count": identification["total"]})

        return result

    def identified_observations_count(self):
        """Return total number (integer) of individual observations identified."""

        qs = Identification.objects.filter(species__isnull=False).values("observation__specimen_label").count()

        return qs

    def observations_count(self):
        """Return total number (integer) of individual observations made."""

        qs = Observation.objects.all().count()

        return qs

    def observations_suborder_count(self):
        """Return list of dictionaries of total numbers of observations of each suborder that have been made.

        For example:
        [{'suborder': 'Caelifera', 'count':30},
        {'suborder': 'Ensifera', 'count':60}]"""

        qs = Identification.objects.values("suborder__suborder").annotate(total=Count("suborder"))

        result = []

        for identification in qs:
            result.append({"suborder": identification["suborder__suborder"], "count": identification["total"]})

        return result

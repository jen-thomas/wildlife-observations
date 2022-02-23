from django.db.models import Count

from .models import Identification


class SpeciesReport:
    def __init__(self):
        pass

    def species_count(self):
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

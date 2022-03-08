from django.db.models import Count, Q

from .models import Identification, Observation, Visit, Site


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

        qs = Identification.objects.filter(species__isnull=False).values("species__latin_name").annotate(
            total=Count("species")).order_by("-total")

        result = []

        for identification in qs:
            result.append({"species_name": identification["species__latin_name"], "count": identification["total"]})

        return result

    def number_confirmed_species_observed(self):
        """Returns the number of confirmed species (integer) that have been recorded."""

        qs = len(set(Identification.objects.filter(Q(confidence=Identification.Confidence.YES) | Q(
            confidence=Identification.Confidence.CONFIRMED)).values_list("species__latin_name", flat=True)))

        return qs

    def number_unconfirmed_species_observed(self):
        """Returns the number of unconfirmed species (integer) that have been recorded."""

        qs = len(set(Identification.objects.values_list("species__latin_name", flat=True)))

        return qs

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


class VisitReport:
    def __init__(self):
        pass

    def summarise_sites(self):
        pass
    
    def summarise_visits(self):
        """Return a list of dictionaries of the number of visits to each site.

        For example:
        [{'site_name': 'TOR01', 'count':3},
        {'site_name': 'TOR02', 'count':4}]"""

        qs = Visit.objects.values("site__site_name").annotate(total=Count("date"))

        result = []

        for visit in qs:
            result.append({"site_name": visit["site__site_name"], "count": visit["total"]})

        return result

    def summarise_suborder_survey(self):
        """Return a list of dictionaries of the number of each suborder on each visit to each site.

        For example:
        [{'visit': 'TOR03 20210719 N1', 'Caelifera':7, 'Ensifera':2, 'Unknown':2},
        {'visit': 'TOR05 20210719 H1', 'Caelifera':17, 'Ensifera':5, 'Unknown':5}]"""

        qs = Identification.objects.values("observation__survey")
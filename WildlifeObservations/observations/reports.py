from re import sub

from django.db.models import Count, Q

from .models import Identification, Observation, Visit, Site, Survey


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
        """Return a list of dictionaries of the number of sites within each study area.

        For example:
        [{'area': 'area1', 'count':10},
        {'area': 'area2', 'count':80}]"""

        qs = Site.objects.values("area").annotate(total=Count("area"))

        result = []

        for site in qs:
            result.append({"area": site["area"], "count": site["total"]})

        return result

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
        [{'survey': 'TOR03 20210719 N1', 'Caelifera':7, 'Ensifera':2, 'Unknown':2},
        {'survey': 'TOR05 20210719 H1', 'Caelifera':17, 'Ensifera':5, 'Unknown':5}]"""

        # qs = Identification.objects.values("observation__survey").annotate(total=Count("suborder"))

        result = []

        for survey in Survey.objects.all().order_by('visit__date', 'visit__site__site_name'):
            row = {}

            # TODO count these identifications of Caelifera and Ensifera for unique observation specimen labels.
            row['survey'] = str(survey)
            row['Caelifera'] = Identification.objects.filter(observation__survey=survey).filter(suborder__suborder='Caelifera').count() # all identifications of Caelifera
            row['Ensifera'] = Identification.objects.filter(observation__survey=survey).filter(suborder__suborder='Ensifera').count() # all identifications of Ensifera

            # row['todo'] = Observation.objects.filter(survey=survey).count() - survey.count()
            # row['todo'] = Identification.objects.filter(observation__survey=survey) -

            all_observation_db_ids_for_this_survey = set(Observation.objects.filter(survey=survey).values_list('id', flat=True))
            all_observation_db_ids_for_this_survey_identified = set(Identification.objects.filter(observation__survey=survey).values_list('observation__id', flat=True))

            observations_not_identified_db_ids = all_observation_db_ids_for_this_survey - all_observation_db_ids_for_this_survey_identified

            # row['observations_not_identified'] = Observation.objects.filter(id__in=list(observations_not_identified_db_ids))
            row['observations_not_identified'] = len(observations_not_identified_db_ids)

            result.append(row)

        return result

    def summarise_survey(self):
        """Return a list of dictionaries of the number of each observations recorded during each survey.

        For example:
        [{'survey': 'TOR03 20210719 N1', 'count':15},
        {'survey': 'TOR05 20210719 H1', 'count':23}]"""

        qs = Observation.objects.values("survey").annotate(total=Count("survey"))

        result = []

        for survey in qs:
            survey_id = survey["observation__survey"]
            survey_obj = Survey.objects.get(id=survey_id)
            result.append({"survey": survey_obj, "count": survey["total"]})

        return result
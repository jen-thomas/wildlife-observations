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

    def unconfirmed_species_observed(self):
        """Returns the number of unconfirmed species (integer) that have been recorded."""

        qs = set(Identification.objects.values_list("species__latin_name", flat=True))

        return qs

    def identified_observations_count(self):
        """Return total number (integer) of individual (unique) observations identified to taxonomic level of family, genus or species."""

        qs_identified_to_family = Identification.objects.filter(family__isnull=False).filter(
            confidence__isnull=False).exclude(
            confidence__exact=Identification.Confidence.IN_PROGRESS)

        distinct_observations_identified = qs_identified_to_family.values_list("observation__specimen_label",
                                                                               flat=True).distinct()

        distinct_observations_identified_count = distinct_observations_identified.count()

        return distinct_observations_identified_count

    def identified_observations_finalised_count(self):
        """Return total number (integer) of individual (unique) observations identified to taxonomic level of family, genus or species, that are finalised."""

        qs_identified_to_family = Identification.objects.filter(
            confidence__isnull=False).exclude(
            confidence__in=(
            Identification.Confidence.IN_PROGRESS, Identification.Confidence.REDO, Identification.Confidence.CHECK,
            Identification.Confidence.CHECK_IN_MUSEUM))

        distinct_observations_finalised_identified = qs_identified_to_family.values_list("observation__specimen_label",
                                                                                         flat=True).distinct()

        distinct_observations_finalised_identified_count = distinct_observations_finalised_identified.count()

        return distinct_observations_finalised_identified_count

    def identified_observations_to_species_count(self):
        """Return total number (integer) of individual observations identified to species."""

        qs_identified_to_species = Identification.objects.filter(species__isnull=False).values(
            "observation__specimen_label")

        identified_to_species_count = qs_identified_to_species.distinct().count()

        return identified_to_species_count

    def identified_observations_to_genus_count(self):
        """Return total number (integer) of individual observations identified to genus."""

        qs_identified_to_genus = Identification.objects.filter(genus__isnull=False).values(
            "observation__specimen_label")

        identified_to_genus_count = qs_identified_to_genus.distinct().count()

        return identified_to_genus_count

    def identified_observations_to_genus_not_species_count(self):
        """Return total number (integer) of individual observations that have been identified to genus, not species.

        Note that this query will likely need to be improved to take into account the identification confidence, given that not all will be certain and some will no doubt be counted here that are incorrect."""

        qs_identified_to_genus = Identification.objects.filter(genus__isnull=False).values_list(
            "observation__specimen_label", flat=True)
        qs_identified_to_species = Identification.objects.filter(species__isnull=False).values_list(
            "observation__specimen_label", flat=True)
        obs_genus_set = set(qs_identified_to_genus)
        obs_species_set = set(qs_identified_to_species)

        genus_not_species = obs_genus_set - obs_species_set
        species_not_genus = obs_species_set - obs_genus_set  # being used as a check only. In theory, this should be 0 if the command to complete the taxonomic hierarchy when selecting the lowest possible in an identification, is working correctly

        return len(genus_not_species)

    def observations_count(self):
        """Return total number (integer) of individual observations made."""

        qs = Observation.objects.all().count()

        return qs

    def observations_suborder_count(self):
        """Return list of dictionaries of total numbers of observations of each suborder that have been made.
        Account for the possibility of multiple identifications of each observation.
        Assume though, that each observation has only been identified as one suborder.

        For example:
        [{'suborder': 'Caelifera', 'count':30},
        {'suborder': 'Ensifera', 'count':60}]"""

        identifications = Identification.objects.all()

        specimen_labels = set()

        c = set()
        e = set()
        todo = set()

        for identification in identifications:
            identification: Identification # explicitely define identification to come from the Identification model so that this is recognised by PyCharm

            if identification.observation.specimen_label in specimen_labels: # makes the specimen labels (observations) unique
                continue

            specimen_labels.add(identification.observation.specimen_label) # add the specimen labels to the set (this also makes sure they are unique)

            if identification.suborder is None:
                todo.add(identification.observation.specimen_label) # identifications that do not have a suborder
            elif identification.suborder.suborder == 'Caelifera':
                c.add(identification.observation.specimen_label)
            elif identification.suborder.suborder == 'Ensifera':
                e.add(identification.observation.specimen_label)
            else:
                assert False

        return {'Caelifera': c, 'Ensifera': e, 'todo': todo}

    def identifications_stage_count(self):
        """Return list of dictionaries of count of identifications of each stage, with each confidence level.

        For example:
        [{'stage': 'Adult', 'count':30},
        {'stage': 'Nymph', 'count':60}]"""

        qs = Identification.objects.values("stage").annotate(total=Count("stage"))

        result = []

        for identification in qs:
            if identification["stage"] != None:
                result.append({"stage": identification["stage"], "count": identification["total"]})

        return result

    def identifications_stage_confidence_count(self):
        """Return list of dictionaries of count of identifications of each stage, with each confidence level.

        For example:
        [{'stage': 'Adult', 'confidence': 'Yes', 'count':30},
        {'stage': 'Adult', 'confidence': 'Checked', 'count':10},
        {'stage': 'Nymph', 'confidence': 'Redo', 'count':60}]"""

        qs = Identification.objects.values("stage", "confidence").annotate(total=Count("stage"))

        result = []

        for identification in qs:
            if identification["stage"] != None:
                result.append({"stage": identification["stage"], "confidence": identification["confidence"],
                               "count": identification["total"]})

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
            row['Caelifera'] = Identification.objects.filter(observation__survey=survey).filter(
                suborder__suborder='Caelifera').count()  # all identifications of Caelifera
            row['Ensifera'] = Identification.objects.filter(observation__survey=survey).filter(
                suborder__suborder='Ensifera').count()  # all identifications of Ensifera

            # row['todo'] = Observation.objects.filter(survey=survey).count() - survey.count()
            # row['todo'] = Identification.objects.filter(observation__survey=survey) -

            all_observation_db_ids_for_this_survey = set(
                Observation.objects.filter(survey=survey).values_list('id', flat=True))
            all_observation_db_ids_for_this_survey_identified = set(
                Identification.objects.filter(observation__survey=survey).values_list('observation__id', flat=True))

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

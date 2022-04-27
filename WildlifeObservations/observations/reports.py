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
        """Return total number (integer) of individual (unique) observations identified to taxonomic level of family,
        genus or species."""

        qs_identified_to_family = Identification.objects.filter(family__isnull=False).filter(
            confidence__isnull=False).exclude(
            confidence__exact=Identification.Confidence.IN_PROGRESS)

        distinct_observations_identified = qs_identified_to_family.values_list("observation__specimen_label",
                                                                               flat=True).distinct()

        distinct_observations_identified_count = distinct_observations_identified.count()

        return distinct_observations_identified_count

    def identified_observations_finalised_count(self):
        """Return total number (integer) of individual (unique) observations identified to taxonomic level of family,
        genus or species, that are finalised."""

        qs_identified_to_family = Identification.objects.filter(
            confidence__isnull=False).exclude(
            confidence__in=(
                Identification.Confidence.IN_PROGRESS, Identification.Confidence.REDO, Identification.Confidence.CHECK,
                Identification.Confidence.CHECK_IN_MUSEUM))

        distinct_observations_finalised_identified = qs_identified_to_family.values_list("observation__specimen_label",
                                                                                         flat=True).distinct()

        distinct_observations_finalised_identified_count = distinct_observations_finalised_identified.count()

        return distinct_observations_finalised_identified_count

    def identified_observations_to_species(self):
        """Return dictionary of individual observations identified to species, with details of the confidence of the
        identification.

        Observations with more than one identification should not be considered more than once, by adding them to a set
        and checking this set before adding another identification for the same observation.

        A hierarchy of "certainty" is used for the confidence level of the identification, which means that confirmed
        identifications will be added to the set before those that are less certain, in cases where an observation has
        multiple identifications with differing certainty.

        TODO: check that observations with multiple identifications that are confirmed, choose the same species / genus.
        """

        identified_to_species = Identification.objects.filter(species__isnull=False)

        # specimen_labels = set()

        # confidence order of hierarchy
        all_confirmed = set()
        all_nymphs_hard_to_id = set()
        all_cannot_id_further = set()
        all_check_in_museum = set()
        all_review = set()
        all_check = set()
        all_redo = set()
        all_in_progress = set()
        all_missing_confirmation = set()

        for identification in identified_to_species:
            identification: Identification

            # if identification.observation.specimen_label in specimen_labels:  # only consider a specimen label if it
            #     # has not already been added to the set. This avoids identifications being considered more than once.
            #     continue
            #
            # specimen_labels.add(identification.observation.specimen_label)  # add the specimen labels to the set

            # the confidences are added in order of concreteness.
            if identification.confidence == Identification.Confidence.YES \
                    or identification.confidence == Identification.Confidence.CONFIRMED:
                all_confirmed.add(identification.observation.specimen_label)  # identifications that are confirmed
            elif identification.confidence == Identification.Confidence.SMALL_NYMPH_HARD_TO_ID:  # this is not really
                # relevant for those that are identified to species, but left in just in case one appears due to a
                # problem with data entry
                all_nymphs_hard_to_id.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.CANNOT_DETERMINE_FURTHER:  # this is not really
                # relevant for those that are identified to species, but left in just in case one appears due to a
                # problem with data entry
                all_cannot_id_further.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.CHECK_IN_MUSEUM:
                all_check_in_museum.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.REVIEW:
                all_review.add(identification.observation.specimen_label)  # identifications that are for review
            elif identification.confidence == Identification.Confidence.CHECK:
                all_check.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.REDO:
                all_redo.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.IN_PROGRESS:
                all_in_progress.add(identification.observation.specimen_label)
            elif identification.confidence is None:
                all_missing_confirmation.add(identification.observation.specimen_label)
            else:
                assert False

        cannot_id_further = all_cannot_id_further - all_confirmed
        check_in_museum = all_check_in_museum - all_confirmed # intentionally leaving out those that cannot be identified further
        review = all_review - all_check_in_museum - all_confirmed
        check = all_check - all_check_in_museum - all_review - all_cannot_id_further - all_confirmed
        redo = all_redo - all_check - all_check_in_museum - all_review - all_cannot_id_further - all_confirmed
        in_progress = all_in_progress - all_redo - all_check - all_check_in_museum - all_review - all_cannot_id_further - all_confirmed
        nymphs_hard_to_id = all_nymphs_hard_to_id - all_confirmed # intentionally removed nymphs that are hard to ID from the other sets

        return {'Confirmed': all_confirmed, 'CannotIDfurther': cannot_id_further, 'NymphsIDhard': nymphs_hard_to_id,
                'Review': review, 'Check': check, 'CheckMuseum': check_in_museum, 'Redo': redo,
                'InProgress': in_progress, 'NoConfirmation': all_missing_confirmation}

    def unique_observations_identified_to_species(self, dict_identifications_to_species):
        """Gets the unique observations identified to species, from a dictionary of sets which
        contains all of the identifications and their confidence level."""

        unique_observations_from_identifications = set()

        for key, specimen_labels in dict_identifications_to_species.items():
            unique_observations_from_identifications.update(specimen_labels)

        return unique_observations_from_identifications

    def identified_observations_to_genus_not_species(self):
        """Return dictionary of observations that have been identified to genus, not species, with details of
        confidence."""

        identified_to_genus = Identification.objects.filter(genus__isnull=False).filter(species__isnull=True)

        total_unique_observations_genus = len(
            set(identified_to_genus.values_list("observation__specimen_label", flat=True)))

        specimen_labels = set()

        nymphs_hard_to_id = set()
        cannot_id_further = set()
        confirmed = set()
        in_progress = set()
        redo = set()
        review = set()
        check = set()
        check_in_museum = set()
        missing_confirmation = set()

        for identification in identified_to_genus:
            identification: Identification

            if identification.observation.specimen_label in specimen_labels:  # only consider a specimen label if it
                # has not already been added to the set
                continue

            specimen_labels.add(identification.observation.specimen_label)  # add the specimen labels to the set

            # the confidences are added in order of concreteness.
            if identification.confidence == Identification.Confidence.CONFIRMED \
                    or identification.confidence == Identification.Confidence.YES:
                confirmed.add(identification.observation.specimen_label)  # identifications that are confirmed
            elif identification.confidence == Identification.Confidence.SMALL_NYMPH_HARD_TO_ID:
                nymphs_hard_to_id.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.CANNOT_DETERMINE_FURTHER:
                cannot_id_further.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.REVIEW:
                review.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.CHECK_IN_MUSEUM:
                check_in_museum.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.CHECK:
                check.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.REDO:
                redo.add(identification.observation.specimen_label)
            elif identification.confidence == Identification.Confidence.IN_PROGRESS:
                in_progress.add(identification.observation.specimen_label)
            elif identification.confidence is None:
                missing_confirmation.add(identification.observation.specimen_label)
            else:
                assert False

        return {'Total': total_unique_observations_genus, 'Confirmed': confirmed, 'CannotIDfurther': cannot_id_further,
                'NymphsIDhard': nymphs_hard_to_id, 'NoConfirmation': missing_confirmation, 'Review': review,
                'Check': check,
                'CheckMuseum': check_in_museum, 'Redo': redo, 'InProgress': in_progress,
                'MissingConfirmation': missing_confirmation}

    def observations_count(self):
        """Return set of individual observations made."""

        qs = Observation.objects.all()
        observations = set()

        for observation in qs:
            observation: Observation

            observations.add(observation.specimen_label)

        return observations

    def observations_suborder(self):
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
            identification: Identification  # explicitely define identification to come from the Identification model
            # so that this is recognised by PyCharm

            if identification.observation.specimen_label in specimen_labels:  # only consider a specimen label if it
                # has not already been added to the set
                continue

            specimen_labels.add(
                identification.observation.specimen_label)  # add the specimen labels to the set (this also makes sure
            # they are unique)

            if identification.suborder is None:
                todo.add(identification.observation.specimen_label)  # identifications that do not have a suborder
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

            observations_not_identified_db_ids = \
                all_observation_db_ids_for_this_survey - all_observation_db_ids_for_this_survey_identified

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

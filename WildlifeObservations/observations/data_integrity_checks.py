from django.db.models import Q, Count

from .models import Identification, Observation, Survey, MeteorologyConditions


class IdentificationDataChecks:
    def __init__(self):
        pass

    def check_identification_has_sex_adults_only(self):
        """
        Returns list of dictionaries of the identifications that do not have a sex, only for the specimens that have
        been noted as adults.

        Note that whilst it might not be possible to determine the sex of an observation if it is not an adult,
        these identifications should still have sex=UNKNOWN, therefore this query considers all identifications,
        not just the adults.

        e.g.    [{"specimen_label": TOR08 20211005 H1 C001},
                {"specimen_label": TAV09 20211006 N1 C008}]
        """

        identifications = Identification.objects.filter(stage=Identification.Stage.ADULT, sex__isnull=True)

        identifications_missing_sex = []

        for identification in identifications:
            identifications_missing_sex.append({"specimen_label": identification.observation.specimen_label})

        return identifications_missing_sex

    def check_identification_has_sex(self):
        """
        Returns list of dictionaries of the identifications that do not have a sex.

        Note that whilst it might not be possible to determine the sex of an observation if it is not an adult,
        these identifications should still have sex=UNKNOWN, therefore this query considers all identifications,
        not just the adults.

        e.g.    [{"specimen_label": TOR08 20211005 H1 C001},
                {"specimen_label": TAV09 20211006 N1 C008}]
        """

        identifications = Identification.objects.filter(sex__isnull=True)

        identifications_missing_sex = []

        for identification in identifications:
            identifications_missing_sex.append({"specimen_label": identification.observation.specimen_label})

        return identifications_missing_sex

    def check_identification_has_stage(self):
        """
        Returns list of dictionaries of the identifications that do not have a stage.

        e.g.    [{"specimen_label": TOR08 20211005 H1 C001},
                {"specimen_label": TAV09 20211006 N1 C008}]
        """

        identifications = Identification.objects.filter(stage__isnull=True)

        identifications_missing_stage = []

        for identification in identifications:
            identifications_missing_stage.append({"specimen_label": identification.observation.specimen_label})

        return identifications_missing_stage

    def check_identification_has_confidence(self):
        """
        Returns list of dictionaries of the identifications that do not have a confidence.

        e.g.    [{"specimen_label": TOR08 20211005 H1 C001},
                {"specimen_label": TAV09 20211006 N1 C008}]
        """

        identifications = Identification.objects.filter(confidence__isnull=True)

        identifications_missing_confidence = []

        for identification in identifications:
            identifications_missing_confidence.append({"specimen_label": identification.observation.specimen_label})

        return identifications_missing_confidence

    def find_observations_without_identification(self):
        """
        Returns a set of the observations that do not have any identifications.
        """

        observations = Observation.objects.all().values_list('specimen_label', flat=True)
        identifications = Identification.objects.all().values_list('observation__specimen_label', flat=True)

        observations_set = set()
        for observation in observations:
            observation: Observation

            observations_set.add(observation)

        identifications_set = set()
        for identification in identifications:
            identification: Identification

            identifications_set.add(identification)  # creating a set of the identifications, deals with the duplicates

        # get all of the observations that do not have the specimen label in the identifications
        observations_without_identifications = observations_set - identifications_set

        return observations_without_identifications

    def add_identifications_to_set(self, set, qs):
        """
        Add identifications from a queryset into a set. Return the set.
        """

        for identification in qs:
            identification: Identification

            set.add(identification)

        return set

    def find_observations_without_confirmed_or_finalised_identification(self):
        """
        Returns a set of the observations that do not have any identifications that have a confidence
        that is confirmed or finalised. This query will only consider observations that have at least one
        identification.
        """

        all_identifications = Identification.objects.all().values_list('observation__specimen_label', flat=True)
        confirmed_identifications = self.get_qs_confirmed_identifications()
        finalised_identifications = self.get_qs_finalised_identifications()

        confirmed_identifications_qs = confirmed_identifications.values_list('observation__specimen_label', flat=True)
        finalised_identifications_qs = finalised_identifications.values_list('observation__specimen_label', flat=True)

        all_identifications_set = set()
        confirmed_identifications_set = set()
        finalised_identifications_set = set()

        all_identifications_set = self.add_identifications_to_set(all_identifications_set, all_identifications)
        confirmed_identifications_set = self.add_identifications_to_set(confirmed_identifications_set,
                                                                        confirmed_identifications_qs)
        finalised_identifications_set = self.add_identifications_to_set(finalised_identifications_set,
                                                                        finalised_identifications_qs)

        observations_without_confirmation_or_finalisation = \
            all_identifications_set - confirmed_identifications_set - finalised_identifications_set  # as this is
        # reduced to distinct specimen labels, these are equivalent to the observations

        return observations_without_confirmation_or_finalisation

    def check_confirmed_identifications_sex(self):
        """
        Returns a set of identifications that have confirmed identifications but the sex in these confirmed
        identifications differs.
        """

        confirmed_identifications = self.get_qs_confirmed_identifications()
        confirmed_identifications_qs = confirmed_identifications.values_list('observation__specimen_label', flat=True)

        confirmed_identifications_different_sex = set()

        for confirmed_identification in confirmed_identifications_qs:
            distinct_sexes = Identification.objects.filter(
                observation__specimen_label=confirmed_identification).values_list('sex').distinct()
            if len(distinct_sexes) > 1:
                confirmed_identifications_different_sex.add(confirmed_identification)

        return confirmed_identifications_different_sex

    def check_confirmed_identifications_stage(self):
        """
        Returns a set of identifications that have confirmed identifications but the stage in these confirmed
        identifications differs.
        """
        confirmed_identifications = self.get_qs_confirmed_identifications()
        confirmed_identifications_qs = confirmed_identifications.values_list('observation__specimen_label', flat=True)

        confirmed_identifications_different_stage = set()

        for confirmed_identification in confirmed_identifications_qs:
            distinct_stages = Identification.objects.filter(
                observation__specimen_label=confirmed_identification).values_list('stage').distinct()
            if len(distinct_stages) > 1:
                confirmed_identifications_different_stage.add(confirmed_identification)

        return confirmed_identifications_different_stage

    def identification_inconsistency(self, identification1, identification2):
        """
        Compares two identifications according to the different levels of taxonomy and return those that are
        inconsistent at the same level. Return dictionary of the inconsistent identifcation with the observation
        specimen label and the field that is inconsistent.

        A non-empty field and null are considered to be inconsistent for the purposes of this function.
        """

        inconsistent_identification = {}

        for field in ['species', 'genus', 'subfamily', 'family', 'suborder']:
            if getattr(identification1, field) != getattr(identification2, field):
                inconsistent_identification['specimen_label'] = identification1.observation.specimen_label
                inconsistent_identification['field'] = field

                return inconsistent_identification

        return None

    def get_qs_confirmed_identifications(self):
        """
        Returns a queryset of all confirmed identifications.
        """
        confirmed_identifications = Identification.objects.filter(confidence=Identification.Confidence.CONFIRMED)

        return confirmed_identifications

    def get_qs_finalised_identifications(self):
        """
        Returns a queryset of all finalised identifications.
        """
        finalised_identifications = Identification.objects.filter(confidence=Identification.Confidence.FINALISED)

        return finalised_identifications

    def get_confirmed_identifications_to_check_taxonomy(self, confirmed_identifications):
        """
        Returns a list of querysets that are the identifications for which more than one identification exists, for a
        particular observation. These are the identifications that need to be compared to check if they have a
        consistent taxonomy.
        """
        multiple_confirmed_identifications_for_observation = confirmed_identifications.values(
            'observation__specimen_label').annotate(number_ids=Count('observation__specimen_label')).filter(
            number_ids__gt=1)

        identifications_to_check = []
        for observation in multiple_confirmed_identifications_for_observation:
            identifications_to_check.append(confirmed_identifications.filter(
                observation__specimen_label=observation['observation__specimen_label']))

        return identifications_to_check

    def check_confirmed_identifications_taxonomy(self):
        """
        Returns a list of dictionaries of the specimen labels which have inconsistent confirmed identifications.
        """
        confirmed_identifications = self.get_qs_confirmed_identifications()

        identifications_to_check = self.get_confirmed_identifications_to_check_taxonomy(confirmed_identifications)

        inconsistent_identifications = []
        for qs_of_identifications in identifications_to_check:
            inconsistent_identification = self.identification_inconsistency(qs_of_identifications[0],
                                                                            qs_of_identifications[1])
            if inconsistent_identification != None:
                inconsistent_identifications.append(inconsistent_identification)

        return inconsistent_identifications


class SurveyDataChecks:
    def __init__(self):
        pass

    def find_surveys_without_met_conditions(self):
        """
        Returns a set of surveys for which there is no meteorological data.
        """

        surveys = Survey.objects.all().values_list('visit__site__site_name', 'visit__date', 'method', 'repeat')
        met_conditions = MeteorologyConditions.objects.all().values_list('survey__visit__site__site_name',
                                                                         'survey__visit__date', 'survey__method',
                                                                         'survey__repeat')

        surveys_set = set()

        for survey in surveys:
            survey: Survey

            surveys_set.add(survey)

        met_conditions_surveys_set = set()

        for surveyed_met_conditions in met_conditions:
            surveyed_met_conditions: MeteorologyConditions

            met_conditions_surveys_set.add(surveyed_met_conditions)

        # get all of the surveys that do not have meteorological condition data
        surveys_without_met_conditions = surveys_set - met_conditions_surveys_set

        return surveys_without_met_conditions

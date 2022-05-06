from django.db.models import Q

from .models import Identification, Observation


class IdentificationDataChecks:
    def __init__(self):
        pass

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

    def find_observations_without_confirmed_identification(self):
        """
        Returns a set of the observations that do not have any identifications that have a confidence
        that is confirmed. This query will only consider observations that have at least one identification.
        """

        all_identifications = Identification.objects.all().values_list('observation__specimen_label', flat=True)
        confirmed_identifications = Identification.objects.filter(
            confidence=Identification.Confidence.CONFIRMED).values_list('observation__specimen_label', flat=True)

        all_identifications_set = set()
        confirmed_identifications_set = set()

        for identification in all_identifications:
            identification: Identification

            all_identifications_set.add(
                identification)  # adding the identifications to the set accounts for the duplicate specimen labels

        for identification in confirmed_identifications:
            identification: Identification

            confirmed_identifications_set.add(
                identification)  # adding the identifications to the set accounts for the duplicate specimen labels

        observations_without_confirmation = all_identifications_set - confirmed_identifications_set  # as this is
        # reduced to distinct specimen labels, these are equivalent to the observations

        return observations_without_confirmation

    def check_confirmed_identifications_sex(self):
        """
        Returns a set of identifications that have confirmed identifications but the sex in these confirmed
        identifications differs.
        """

        confirmed_identifications = Identification.objects.filter(confidence=Identification.Confidence.CONFIRMED).values_list('observation__specimen_label', flat=True)

        confirmed_identifications_different_sex = set()

        for confirmed_identification in confirmed_identifications:
            distinct_sexes = Identification.objects.filter(observation__specimen_label=confirmed_identification).values_list('sex').distinct()
            if len(distinct_sexes) > 1:
                confirmed_identifications_different_sex.add(confirmed_identification)

        return confirmed_identifications_different_sex

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


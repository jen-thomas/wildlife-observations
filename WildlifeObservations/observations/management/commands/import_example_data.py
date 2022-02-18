from django.core.management.base import BaseCommand

from ...models import TaxonomyClass, TaxonomyOrder, TaxonomySuborder, TaxonomyFamily, TaxonomySpecies, \
    Site, Visit, Survey, Observation, Identification, IdentificationGuide, Plot, MeteorologyConditions, \
    VegetationStructure, TaxonomyGenus

from django.db import transaction


class Command(BaseCommand):
    help = 'Adds a set of example data'

    @transaction.atomic
    def handle(self, *args, **options):
        import_species()
        import_visits()
        import_identifications()


def import_visits():
    catalonia_a = Site.objects.create(area='Catalonia', site_name='CAT01', altitude_band='1800',
                                      gps_latitude_start=42.2669, gps_longitude_start=1.7812, gps_altitude_start=1826,
                                      gps_latitude_end=42.3, gps_longitude_end=1.7822, gps_altitude_end=1885,
                                      transect_length=100)
    catalonia_b = Site.objects.create(area='Catalonia', site_name='CAT02', altitude_band='1900',
                                      gps_latitude_start=42.2626, gps_longitude_start=1.8015, gps_altitude_start=1986,
                                      gps_latitude_end=42.28, gps_longitude_end=1.8035, gps_altitude_end=1974,
                                      transect_length=100)
    catalonia_c = Site.objects.create(area='Catalonia', site_name='CAT03', altitude_band='2000',
                                      gps_latitude_start=42.2795, gps_longitude_start=1.7857, gps_altitude_start=2014,
                                      gps_latitude_end=42.3, gps_longitude_end=1.8, gps_altitude_end=2015,
                                      transect_length=100)

    visit_sept = Visit.objects.create(site=catalonia_a, date='2021-09-17')
    visit_july = Visit.objects.create(site=catalonia_b, date='2021-07-17')

    survey_july_net = Survey.objects.create(visit=visit_july, start_time='12:10:00', end_time='12:20:00', method='Net',
                                            repeat='1', observer='Person B')
    survey_july_hand = Survey.objects.create(visit=visit_july, start_time='12:30:00', end_time='12:40:00',
                                             method='Hand', repeat='1', observer='Person B')
    survey_sept_net = Survey.objects.create(visit=visit_sept, start_time='11:10:00', end_time='11:20:00', method='Net',
                                            repeat='1', observer='Person A')
    survey_sept_hand = Survey.objects.create(visit=visit_sept, start_time='13:10:00', end_time='13:20:00',
                                             method='Hand', repeat='1', observer='Person A')

    Observation.objects.create(survey=survey_sept_net, specimen_label='CAT01 20210917 N1 C001', status='Specimen')
    Observation.objects.create(survey=survey_july_hand, specimen_label='CAT01 20210717 H1 E001', status='Specimen')
    Observation.objects.create(survey=survey_sept_hand, specimen_label='CAT01 20210917 H1 E001', status='Specimen')
    Observation.objects.create(survey=survey_sept_hand, specimen_label='CAT01 20210917 H1 E002', status='Specimen')
    Observation.objects.create(survey=survey_july_net, specimen_label='CAT01 20210717 N1 C001', status='Specimen')
    Observation.objects.create(survey=survey_july_net, specimen_label='CAT01 20210717 N1 C002', status='Specimen')
    Observation.objects.create(survey=survey_july_net, specimen_label='CAT01 20210717 N1 C003', status='Specimen')

    plot10_survey_july = Plot.objects.create(visit=visit_july, position=10)

    VegetationStructure.objects.create(plot=plot10_survey_july, percentage_vegetation_cover=10, percentage_rock=10,
                                       percentage_bare_ground=80, height_75percent=30, max_height=40, density_01=5,
                                       density_02=5, density_03=10, density_04=1, density_05=7)

    MeteorologyConditions.objects.create(survey=survey_july_hand, cloud_coverage_start=0, wind_start=0, rain_start=0,
                                         cloud_coverage_end=1, wind_end=1, rain_end=0)


def import_species():
    insecta_class = TaxonomyClass.objects.create(taxclass='Insecta')
    order = TaxonomyOrder.objects.create(order='Orthoptera', taxclass=insecta_class)
    suborder_ensifera = TaxonomySuborder.objects.create(order=order, suborder='Ensifera')
    suborder_caelifera = TaxonomySuborder.objects.create(order=order, suborder='Caelifera')
    family_tett = TaxonomyFamily.objects.create(suborder=suborder_ensifera, family='Tettigoniidae')
    family_acrididae = TaxonomyFamily.objects.create(suborder=suborder_caelifera, family='Acrididae')
    genus_leptophyes = TaxonomyGenus.objects.create(family=family_tett, genus='Leptophyes')
    genus_omocestus = TaxonomyGenus.objects.create(family=family_acrididae, genus='Omocestus')
    TaxonomySpecies.objects.create(genus=genus_leptophyes, latin_name='Leptophyes punctatissima',
                                   common_name_english='Speckled bush-cricket')
    TaxonomySpecies.objects.create(genus=genus_omocestus, latin_name='Omocestus antigai',
                                   common_name_english='Pyrenean grasshopper',
                                   common_name_catalan='Saltamartí català')


def import_identifications():
    id_guide = IdentificationGuide.objects.create(title='Grasshoppers of Britain and Western Europe',
                                                  author='Sardet, Roesti and Braud')

    Identification.objects.create(observation=Observation.objects.get(specimen_label='CAT01 20210917 N1 C001'),
                                  species=TaxonomySpecies.objects.get(latin_name='Omocestus antigai'), sex='Male',
                                  stage='Adult', identification_guide=id_guide, date_of_identification='2021-12-01',
                                  confidence='Check')
    Identification.objects.create(observation=Observation.objects.get(specimen_label='CAT01 20210917 H1 E001'),
                                  species=TaxonomySpecies.objects.get(latin_name='Leptophyes punctatissima'),
                                  sex='Female', stage='Adult', identification_guide=id_guide,
                                  date_of_identification='2021-12-01', confidence='Confirmed')
    Identification.objects.create(observation=Observation.objects.get(specimen_label='CAT01 20210917 H1 E002'),
                                  species=TaxonomySpecies.objects.get(latin_name='Leptophyes punctatissima'),
                                  sex='Female', stage='Adult', identification_guide=id_guide,
                                  date_of_identification='2021-12-01', confidence='Confirmed')

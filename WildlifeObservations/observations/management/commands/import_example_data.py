from django.core.management.base import BaseCommand

from ...models import TaxonomyClass, TaxonomyOrder, TaxonomySuborder, TaxonomyFamily, TaxonomySpecies, SpeciesName, \
    Site, Visit, Survey, Observation, Identification, IdentificationGuide


class Command(BaseCommand):
    help = 'Adds a set of example data'

    def handle(self, *args, **options):
        import_species()
        import_visits()
        import_identifications()


def import_visits():
    catalonia_a = Site.objects.create(area='Catalonia', site_name='CAT01', altitude_band='1800')
    catalonia_b = Site.objects.create(area='Catalonia', site_name='CAT02', altitude_band='1900')
    catalonia_c = Site.objects.create(area='Catalonia', site_name='CAT03', altitude_band='2000')

    visit_sept = Visit.objects.create(site_name=catalonia_a, date='2021-09-17')
    visit_july = Visit.objects.create(site_name=catalonia_b, date='2021-07-17')

    survey_july_net = Survey.objects.create(visit=visit_july, start_time='12:10:00', end_time='12:20:00', method='Net',
                                            repeat='1', observer='Person B')
    survey_july_hand = Survey.objects.create(visit=visit_july, start_time='12:30:00', end_time='12:40:00',
                                             method='Hand', repeat='1', observer='Person B')
    survey_sept_net = Survey.objects.create(visit=visit_sept, start_time='11:10:00', end_time='11:20:00', method='Net',
                                            repeat='1', observer='Person A')
    survey_sept_hand = Survey.objects.create(visit=visit_sept, start_time='13:10:00', end_time='13:20:00',
                                             method='Hand', repeat='1', observer='Person A')

    Observation.objects.create(survey=survey_sept_net, specimen_id='CAT01 20210917 N1 C001', status='Specimen')
    Observation.objects.create(survey=survey_july_hand, specimen_id='CAT01 20210717 H1 E001', status='Specimen')
    Observation.objects.create(survey=survey_sept_hand, specimen_id='CAT01 20210917 H1 E001', status='Specimen')
    Observation.objects.create(survey=survey_sept_hand, specimen_id='CAT01 20210917 H1 E002', status='Specimen')
    Observation.objects.create(survey=survey_july_net, specimen_id='CAT01 20210717 N1 C001', status='Specimen')
    Observation.objects.create(survey=survey_july_net, specimen_id='CAT01 20210717 N1 C002', status='Specimen')
    Observation.objects.create(survey=survey_july_net, specimen_id='CAT01 20210717 N1 C003', status='Specimen')


def import_species():
    insecta_class = TaxonomyClass.objects.create(taxclass='Insecta')
    order = TaxonomyOrder.objects.create(order='Orthoptera', taxclass=insecta_class)
    suborder_ensifera = TaxonomySuborder.objects.create(order=order, suborder='Ensifera')
    suborder_caelifera = TaxonomySuborder.objects.create(order=order, suborder='Caelifera')
    family_tett = TaxonomyFamily.objects.create(suborder=suborder_ensifera, family='Tettigoniidae')
    family_acrididae = TaxonomyFamily.objects.create(suborder=suborder_caelifera, family='Acrididae')
    species_leptophyes = TaxonomySpecies.objects.create(family=family_tett, latin_name='Leptophyes punctatissima')
    species_omocestus = TaxonomySpecies.objects.create(family=family_acrididae, latin_name='Omocestus antigai')
    SpeciesName.objects.create(species=species_leptophyes, common_name_english='Speckled bush-cricket')
    SpeciesName.objects.create(species=species_omocestus, common_name_english='Pyrenean grasshopper')


def import_identifications():
    id_guide = IdentificationGuide.objects.create(title='Grasshoppers of Britain and Western Europe',
                                                  author='Sardet, Roesti and Braud')

    Identification.objects.create(specimen_id='CAT01 20210917 N1 C001', species='Omocestus antigai', sex='Male',
                                  stage='Adult', identification_guide=id_guide)
    Identification.objects.create(specimen_id='CAT01 20210917 H1 E001', species='Leptophyes punctatissima',
                                  sex='Female', stage='Adult', identification_guide=id_guide)
    Identification.objects.create(specimen_id='CAT01 20210917 H1 E002', species='Leptophyes punctatissima',
                                  sex='Female', stage='Adult', identification_guide=id_guide)
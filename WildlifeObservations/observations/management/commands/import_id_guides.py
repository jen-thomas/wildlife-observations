from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import IdentificationGuide

class Command(BaseCommand):
    help = 'Adds ID guides'

    @transaction.atomic
    def handle(self, *args, **options):
        self.import_id_guides()

    def import_id_guides(self):
        id_guide = IdentificationGuide.objects.create(title='Grasshoppers of Britain and Western Europe',
                                                  author='Sardet, Roesti and Braud')
        id_guide = IdentificationGuide.objects.create(title='The Orthoptera fauna of the Pyrenean region - a field guide',
                                                      author='Poniatowski, Defaut, Llucià-Pomares and Fartmann')
        id_guide = IdentificationGuide.objects.create(title='Atles dels Ortòpters de Catalunya',
                                                      author='Olmo Vidal')
        id_guide = IdentificationGuide.objects.create(title='Revisión de los Ortópteros (Insecta: Orthoptera) de Cataluña (España)',
                                                      author='Llucià Pomares')
        id_guide = IdentificationGuide.objects.create(
            title='Saltamontes, Grillos y Langostas',
            author='Bellmann, Rutschmann, Roesti and Hochkirch')
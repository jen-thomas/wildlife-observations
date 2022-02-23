from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import TaxonomySpecies, TaxonomyGenus, TaxonomySuborder, TaxonomyFamily, TaxonomyClass, TaxonomyOrder
import csv


class Command(BaseCommand):
    help = 'Adds taxonomy'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        print(options['filename'])
        self.import_taxonomy_from_csv(options['filename'])

    def import_species_from_csv(self, row_data, genus):
        
        catalan = string_or_none(row_data['catalan'])
        english = string_or_none(row_data['english'])
        spanish = string_or_none(row_data['spanish'])

        species, created = TaxonomySpecies.objects.get_or_create(genus=genus, latin_name=row_data['species'],
                                                                 common_name_catalan=catalan,
                                                                 common_name_english=english,
                                                                 common_name_spanish=spanish)

        return species

    def import_genus_from_csv(self, row_data, family):
        genus, created = TaxonomyGenus.objects.get_or_create(family=family, genus=row_data['genus'])

        return genus

    def import_family_from_csv(self, row_data, suborder):
        family, created = TaxonomyFamily.objects.get_or_create(suborder=suborder, family=row_data['family'])

        return family

    def import_class(self):
        taxclass, created = TaxonomyClass.objects.get_or_create(taxclass='Insecta')

        taxclass.save()

    def import_order(self):
        order, created = TaxonomyOrder.objects.get_or_create(order='Orthoptera',
                                                             taxclass=TaxonomyClass.objects.get(taxclass='Insecta'))

        order.save()

    def import_taxonomy_from_csv(self, filename):
        self.import_class()
        self.import_order()

        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                suborder, created = TaxonomySuborder.objects.get_or_create(suborder=row['suborder'],
                                                                           order=TaxonomyOrder.objects.get(
                                                                               order='Orthoptera'))
                suborder.save()

                family_data = select_columns(row, ["family"])
                family = self.import_family_from_csv(family_data, suborder)

                genus_data = select_columns(row, ["genus"])
                genus = self.import_genus_from_csv(genus_data, family)

                species_data = select_columns(row, ["species"])
                self.import_species_from_csv(species_data, genus)


def select_columns(row, list_of_columns) -> dict:
    selected = {}

    for column_name in list_of_columns:
        selected[column_name] = row[column_name]

    return selected


def string_or_none(string):
    if string != '':
        output = string
    else:
        output = None

    return output
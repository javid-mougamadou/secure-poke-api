import requests
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate the Group table from the PokeAPI type list'

    def fetch_types(self):
        response = requests.get(f'{settings.POKEAPI_BASE_URL}/api/v2/type')
        response.raise_for_status()
        return response.json()['results']

    def insert_types(self, results):
        for result in results:
            group, created = Group.objects.get_or_create(name=result['name'])
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'{status}: {group.name}')

    def handle(self, *args, **kwargs):
        results = self.fetch_types()
        self.insert_types(results)

import requests
from django.conf import settings

from .entities import Pokemon, PokemonReference


def get_pokemons_by_type(type_name):
    url = f'{settings.POKEAPI_BASE_URL}/api/v2/type/{type_name}'
    response = requests.get(url)
    response.raise_for_status()
    return [PokemonReference.from_dict(item['pokemon']) for item in response.json()['pokemon']]


def get_pokemon(id_or_name):
    url = f'{settings.POKEAPI_BASE_URL}/api/v2/pokemon/{id_or_name}'
    response = requests.get(url)
    response.raise_for_status()
    return Pokemon.from_dict(response.json())

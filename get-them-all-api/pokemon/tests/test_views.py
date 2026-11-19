from unittest.mock import Mock

import requests

from clients.access_management_api.entities import CurrentUser
from clients.pokeapi.entities import Pokemon, PokemonReference


class TestPokemonListAPIView:
    def test_request_pokemon_list_no_auth_header_failed(self, client):
        res = client.get('/api/pokemon/')
        assert res.status_code == 401

    def test_request_pokemon_list_invalid_token_failed(self, client, monkeypatch):
        def fake_get_current_user(authorization_header):
            raise requests.exceptions.HTTPError(response=Mock(status_code=401))

        monkeypatch.setattr('clients.access_management_api.helpers.get_current_user', fake_get_current_user)

        res = client.get('/api/pokemon/', HTTP_AUTHORIZATION='Bearer invalid')
        assert res.status_code == 401

    def test_request_pokemon_list_forbidden_token_failed(self, client, monkeypatch):
        def fake_get_current_user(authorization_header):
            raise requests.exceptions.HTTPError(response=Mock(status_code=403))

        monkeypatch.setattr('clients.access_management_api.helpers.get_current_user', fake_get_current_user)

        res = client.get('/api/pokemon/', HTTP_AUTHORIZATION='Bearer forbidden')
        assert res.status_code == 403

    def test_request_pokemon_list_management_api_unavailable_failed(self, client, monkeypatch):
        def fake_get_current_user(authorization_header):
            raise requests.exceptions.ConnectionError()

        monkeypatch.setattr('clients.access_management_api.helpers.get_current_user', fake_get_current_user)

        res = client.get('/api/pokemon/', HTTP_AUTHORIZATION='Bearer sometoken')
        assert res.status_code == 503

    def test_request_pokemon_list_pokeapi_unavailable_failed(self, client, monkeypatch):
        monkeypatch.setattr(
            'clients.access_management_api.helpers.get_current_user',
            lambda authorization_header: CurrentUser(id=1, username='testuser', email='', groups=['fire']),
        )

        def fake_get_pokemons_by_type(type_name):
            raise requests.exceptions.ConnectionError()

        monkeypatch.setattr('pokemon.views.get_pokemons_by_type', fake_get_pokemons_by_type)

        res = client.get('/api/pokemon/', HTTP_AUTHORIZATION='Bearer sometoken')
        assert res.status_code == 503

    def test_request_pokemon_list_success(self, client, monkeypatch):
        monkeypatch.setattr(
            'clients.access_management_api.helpers.get_current_user',
            lambda authorization_header: CurrentUser(id=1, username='testuser', email='', groups=['fire']),
        )

        def fake_get_pokemons_by_type(type_name):
            return [
                PokemonReference(name='charmander', url='https://pokeapi.co/api/v2/pokemon/4/'),
                PokemonReference(name='charizard', url='https://pokeapi.co/api/v2/pokemon/6/'),
            ]

        monkeypatch.setattr('pokemon.views.get_pokemons_by_type', fake_get_pokemons_by_type)

        res = client.get('/api/pokemon/', HTTP_AUTHORIZATION='Bearer sometoken')
        assert res.status_code == 200
        assert res.json() == [
            {'id': 4, 'name': 'charmander'},
            {'id': 6, 'name': 'charizard'},
        ]

    def test_request_pokemon_list_multiple_types_deduplicates_success(self, client, monkeypatch):
        monkeypatch.setattr(
            'clients.access_management_api.helpers.get_current_user',
            lambda authorization_header: CurrentUser(id=1, username='testuser', email='', groups=['fire', 'flying']),
        )

        def fake_get_pokemons_by_type(type_name):
            # charizard (id=6) belongs to both fire and flying
            if type_name == 'fire':
                return [
                    PokemonReference(name='charmander', url='https://pokeapi.co/api/v2/pokemon/4/'),
                    PokemonReference(name='charizard', url='https://pokeapi.co/api/v2/pokemon/6/'),
                ]
            return [
                PokemonReference(name='charizard', url='https://pokeapi.co/api/v2/pokemon/6/'),
                PokemonReference(name='pidgey', url='https://pokeapi.co/api/v2/pokemon/16/'),
            ]

        monkeypatch.setattr('pokemon.views.get_pokemons_by_type', fake_get_pokemons_by_type)

        res = client.get('/api/pokemon/', HTTP_AUTHORIZATION='Bearer sometoken')
        assert res.status_code == 200
        pokemons = res.json()
        assert len(pokemons) == len({pokemon['id'] for pokemon in pokemons})
        assert sorted(pokemons, key=lambda p: p['id']) == [
            {'id': 4, 'name': 'charmander'},
            {'id': 6, 'name': 'charizard'},
            {'id': 16, 'name': 'pidgey'},
        ]


class TestPokemonDetailAPIView:
    def test_request_pokemon_detail_no_auth_header_failed(self, client):
        res = client.get('/api/pokemon/charizard/')
        assert res.status_code == 401

    def test_request_pokemon_detail_authorized_type_success(self, client, monkeypatch):
        monkeypatch.setattr(
            'clients.access_management_api.helpers.get_current_user',
            lambda authorization_header: CurrentUser(id=1, username='testuser', email='', groups=['fire']),
        )

        def fake_get_pokemon(id_or_name):
            return Pokemon(
                id=6,
                name='charizard',
                types=['fire', 'flying'],
            )

        monkeypatch.setattr('pokemon.views.get_pokemon', fake_get_pokemon)

        res = client.get('/api/pokemon/charizard/', HTTP_AUTHORIZATION='Bearer sometoken')
        assert res.status_code == 200
        assert res.json() == {'id': 6, 'name': 'charizard', 'types': ['fire', 'flying']}

    def test_request_pokemon_detail_unauthorized_type_failed(self, client, monkeypatch):
        monkeypatch.setattr(
            'clients.access_management_api.helpers.get_current_user',
            lambda authorization_header: CurrentUser(id=1, username='testuser', email='', groups=['fire']),
        )

        def fake_get_pokemon(id_or_name):
            return Pokemon(
                id=1,
                name='bulbasaur',
                types=['grass'],
            )

        monkeypatch.setattr('pokemon.views.get_pokemon', fake_get_pokemon)

        res = client.get('/api/pokemon/bulbasaur/', HTTP_AUTHORIZATION='Bearer sometoken')
        assert res.status_code == 403

    def test_request_pokemon_detail_not_found_failed(self, client, monkeypatch):
        monkeypatch.setattr(
            'clients.access_management_api.helpers.get_current_user',
            lambda authorization_header: CurrentUser(id=1, username='testuser', email='', groups=['fire']),
        )

        def fake_get_pokemon(id_or_name):
            raise requests.exceptions.HTTPError(response=Mock(status_code=404))

        monkeypatch.setattr('pokemon.views.get_pokemon', fake_get_pokemon)

        res = client.get('/api/pokemon/notapokemon/', HTTP_AUTHORIZATION='Bearer sometoken')
        assert res.status_code == 404

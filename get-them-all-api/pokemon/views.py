import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from clients.access_management_api.helpers import authenticate
from clients.pokeapi.client import get_pokemon, get_pokemons_by_type

from .serializers import PokemonDetailSerializer, PokemonSerializer


class PokemonListAPIView(APIView):
    def get(self, request):
        """
        pokemon_list

        A View for listing the Pokemons the current user has access to, depending on their types
        """
        # Authenticate the user
        current_user, error_response = authenticate(request)
        if error_response:
            return error_response

        # Get pokemons without duplicates
        pokemons_by_id = {}
        try:
            for group in current_user.groups:
                for pokemon in get_pokemons_by_type(group):
                    pokemons_by_id[pokemon.id] = pokemon

        # Handle errors
        except requests.exceptions.HTTPError:
            return Response({'detail': 'PokeAPI error.'}, status=502)
        except requests.exceptions.RequestException:
            return Response({'detail': 'PokeAPI is unavailable.'}, status=503)

        serializer = PokemonSerializer(pokemons_by_id.values(), many=True)
        return Response(serializer.data)


class PokemonDetailAPIView(APIView):
    def get(self, request, id_or_name):
        """
        pokemon_detail

        A View for retrieving a Pokemon, if its type is one the current user has access to
        """
        # Authenticate the user
        current_user, error_response = authenticate(request)
        if error_response:
            return error_response

        # Get the pokemon
        try:
            pokemon = get_pokemon(id_or_name)

        # Handle errors
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return Response({'detail': 'Pokemon not found.'}, status=404)
            return Response({'detail': 'PokeAPI error.'}, status=502)
        except requests.exceptions.RequestException:
            return Response({'detail': 'PokeAPI is unavailable.'}, status=503)

        # Check if the user has access to the pokemon
        if not set(pokemon.types) & set(current_user.groups):
            return Response({'detail': 'You do not have access to this Pokemon.'}, status=403)

        serializer = PokemonDetailSerializer(pokemon)
        return Response(serializer.data)

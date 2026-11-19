from rest_framework import serializers


class PokemonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class PokemonDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    types = serializers.ListField(child=serializers.CharField())

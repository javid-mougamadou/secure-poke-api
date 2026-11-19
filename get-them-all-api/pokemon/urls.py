from django.urls import path

from .views import PokemonDetailAPIView, PokemonListAPIView

urlpatterns = [
    path('pokemon/', PokemonListAPIView.as_view(), name='pokemon-list'),
    path('pokemon/<str:id_or_name>/', PokemonDetailAPIView.as_view(), name='pokemon-detail'),
]

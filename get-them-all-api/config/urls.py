from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi, views
from rest_framework import permissions

schema_view = views.get_schema_view(
    openapi.Info(
        title='Pokemon API',
        default_version='v1',
        description='Pokemon API for SecurePokeAPI',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Django Rest Framework Api Url
    path('api/', include('pokemon.urls')),
    # Swagger Urls
    path(
        r'swagger(<format>\.json|\.yaml)',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

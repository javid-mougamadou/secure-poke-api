from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# Postgres Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# PokeAPI
POKEAPI_BASE_URL = env('POKEAPI_BASE_URL', default='https://pokeapi.co')

# Access management API
ACCESS_MANAGEMENT_API_URL = env('ACCESS_MANAGEMENT_API_URL', default='http://access-management-api:8000')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'get-them-all-api']

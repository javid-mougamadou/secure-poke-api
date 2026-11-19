import requests
from django.conf import settings

from .entities import CurrentUser


def get_current_user(authorization_header):
    response = requests.get(
        f'{settings.ACCESS_MANAGEMENT_API_URL}/api/user/me/',
        headers={'Authorization': authorization_header},
    )
    response.raise_for_status()
    return CurrentUser.from_dict(response.json())

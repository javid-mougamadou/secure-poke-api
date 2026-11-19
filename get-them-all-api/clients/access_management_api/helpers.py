import requests
from rest_framework.response import Response

from .client import get_current_user


def authenticate(request):
    """
    Returns (current_user, None) on success, or (None, error_response) on failure.
    """
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Bearer '):
        return None, Response(
            {'detail': 'Authorization header with Bearer token is required.'},
            status=401,
        )

    try:
        current_user = get_current_user(authorization_header)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return None, Response({'detail': 'Invalid or expired token.'}, status=401)
        if e.response.status_code == 403:
            return None, Response({'detail': 'Forbidden.'}, status=403)
        return None, Response({'detail': 'Access management API error.'}, status=502)
    except requests.exceptions.RequestException:
        return None, Response({'detail': 'Access management API is unavailable.'}, status=503)

    return current_user, None

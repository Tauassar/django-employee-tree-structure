import requests

from django.conf import settings


def get_user_ip(request):
    if request.META.get('HTTP_HOST'):
        ip = request.META.get('HTTP_HOST')
    else:
        ip = ''
    return ip


def verify_token_at_auth_server(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        response = requests.post(f'http://{settings.AUTH_SERVER_LOCATION}/api/auth/token/verify', {'token': token})
        return response.status_code == 200
    except ConnectionError as e:
        return False


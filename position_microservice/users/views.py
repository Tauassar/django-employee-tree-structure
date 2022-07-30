from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .serializers import UserSerializer
from .utils import get_user_ip, verify_token_at_auth_server
from django.conf import settings


class AuthServerOrIsAuthenticatedAtAuthServer(permissions.BasePermission):
    """
    TODO:
    * Change permission check to authentication check
    """
    def has_permission(self, request, view):
        if get_user_ip(request) == settings.AUTH_SERVER_LOCATION:
            return True
        else:
            return verify_token_at_auth_server(request)


class UserViewSet(
    viewsets.ModelViewSet
):
    queryset = User.objects.all()
    permission_classes = [AuthServerOrIsAuthenticatedAtAuthServer]
    serializer_class = UserSerializer

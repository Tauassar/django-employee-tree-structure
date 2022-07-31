from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .serializers import CreateUserSerializer, GetUserSerializer
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
    lookup_field = 'username'  # default is id
    permission_classes = [AuthServerOrIsAuthenticatedAtAuthServer]
    serializer_classes = {
        'default': GetUserSerializer,
        'create': CreateUserSerializer,
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_classes[self.action]
        return self.serializer_classes['default']

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

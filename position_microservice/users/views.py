from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .serializers import UserSerializer
from .utils import get_user_ip
from ..position_microservice.settings import AUTH_SERVER_LOCATION


class AuthServerOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return (get_user_ip(request) == AUTH_SERVER_LOCATION
                or super(AuthServerOrIsAuthenticated, self).has_permission(request, view))


class UserViewSet(
    viewsets.ModelViewSet
):
    queryset = User.objects.all()
    # permission_classes = [CreateOrIsAuthenticated]
    permission_classes = []
    serializer_class = UserSerializer

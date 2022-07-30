import requests

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .serializers import GetUserSerializer, CreateUserSerializer


class CreateOrIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (view.action == 'create'
                or super(CreateOrIsAuthenticated, self).has_permission(request, view))


class UserViewSet(
    viewsets.ModelViewSet
):
    queryset = User.objects.all()
    # permission_classes = [CreateOrIsAuthenticated]
    permission_classes = []
    serializer_classes = {
        'default': GetUserSerializer,
        'create': CreateUserSerializer,
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_classes[self.action]
        return self.serializer_classes['default']

    def create(self, request, *args, **kwargs):
        requests.post()
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):

        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        return super(UserViewSet, self).update(request, *args, **kwargs)

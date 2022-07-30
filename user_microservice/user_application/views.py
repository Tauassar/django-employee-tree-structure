import json

import requests

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets, permissions

from .serializers import GetUserSerializer, CreateUserSerializer
from django.conf import settings


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
        resp = super(UserViewSet, self).create(request, *args, **kwargs)
        if resp.status_code == 201:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            requests.post(
                f'http://{settings.POSITION_SERVER_ADDRESS}/api/user/',
                headers={
                    'content-type': 'application/json',
                    "Authorization": f'Bearer {token}'
                },
                data=json.dumps(request.data)
            )
        return resp

    def destroy(self, request, *args, **kwargs):

        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        return super(UserViewSet, self).update(request, *args, **kwargs)

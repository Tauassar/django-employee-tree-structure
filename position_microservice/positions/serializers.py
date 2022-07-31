from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Node


class PositionsNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

    user = SlugRelatedField(slug_field="username", queryset=User.objects.all())

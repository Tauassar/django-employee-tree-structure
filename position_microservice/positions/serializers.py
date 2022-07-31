from rest_framework import serializers

from .models import Node


class PositionsNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

    username = serializers.SerializerMethodField("get_username", read_only=True)

    def get_username(self, obj):
        if obj.node_type == Node.NodeType.PEOPLE:
            return obj.user.username
        else:
            return ''


class PutPositionsNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        exclude = ['parent']


class MovePositionNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['parent']


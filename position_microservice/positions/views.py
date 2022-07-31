from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Node
from .serializers import PositionsNodeSerializer, PutPositionsNodeSerializer, MovePositionNodeSerializer


def index(request):
    return render(request, 'positions/index.html')


class PositionNodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_classes = {
        'default': PositionsNodeSerializer,
        'update': PutPositionsNodeSerializer,
    }

    def get_serializer_class(self):
        if self.action == 'update':
            return self.serializer_classes[self.action]
        return self.serializer_classes['default']

    def perform_destroy(self, instance):
        Node.delete_node(instance)

    @action(methods=["get"], detail=False)
    def origins(self, request, *args, **kwargs):
        queryset = Node.get_all_tree_origins()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True, name='node-children')
    def child(self, request, pk, *args, **kwargs):
        node = Node.objects.get(id=pk)
        queryset = Node.get_child_nodes(node)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["put"],
        detail=True,
        serializer_classes=MovePositionNodeSerializer,
        name='node-move-with-children')
    def move_with_child(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        methods=["put"],
        detail=True,
        serializer_classes=MovePositionNodeSerializer,
        name='node-move-without-children')
    def move_without_child(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        Node.bind_child_nodes_to_parent(instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["get"], detail=True, name='node-descendants')
    def descendants(self, request, pk, *args, **kwargs):
        node = Node.objects.get(id=pk)
        queryset = Node.get_descendants(node)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=True, name='node-ancestors')
    def ancestors(self, request, pk, *args, **kwargs):
        node = Node.objects.get(id=pk)
        queryset = Node.get_ancestors(node)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

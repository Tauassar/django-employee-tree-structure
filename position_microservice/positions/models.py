from itertools import chain
from django.db import models, transaction, IntegrityError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Node(models.Model):
    """
        Implementation of adjacent list model
    """
    class NodeType(models.TextChoices):
        PEOPLE = 'PL', _('People')
        ORGANISATION = 'ORG', _('Organisational unit')

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    node_type = models.CharField(
        choices=NodeType.choices,
        default=NodeType.PEOPLE,
        max_length=20
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def get_self_name(self):
        if self.node_type == self.NodeType.PEOPLE:
            return f'{self.user.username}'
        else:
            return f'{self.org_unit.name}'

    def __str__(self):
        try:
            if self.node_type == self.NodeType.PEOPLE:
                return f'ID {self.id} {self.parent.get_self_name()} - {self.user.username}'
            else:
                return f'ID {self.id} {self.parent.get_self_name()} - {self.name}'
        except AttributeError:
            if self.node_type == self.NodeType.PEOPLE:
                return f'ID {self.id} {self.user.username}'
            else:
                return f'ID {self.id} {self.name}'

    @staticmethod
    def get_descendants(node):
        queryset = Node.objects.filter(parent=node)
        results = chain(queryset)
        for child in queryset:
            results = chain(results, node.get_descendants(child))
        return results

    @staticmethod
    def get_ancestors(node):
        if node.parent:
            return chain([node.parent], node.get_ancestors(node.parent))
        return chain()

    @staticmethod
    def get_all_tree_origins():
        return Node.objects.filter(parent=None)

    @staticmethod
    def get_child_nodes(node):
        return Node.objects.filter(parent=node)

    @staticmethod
    def bind_child_nodes_to_parent(node):
        try:
            Node.objects.filter(parent=node).update(parent=node.parent)
        except IntegrityError:
            raise IntegrityError('Failed to update node instance\'s child nodes')

    @staticmethod
    def delete_node(node):
        with transaction.atomic():
            Node.bind_child_nodes_to_parent(node)
            node.delete()

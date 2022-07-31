from itertools import chain
from django.db import models
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
                return f'{self.parent.get_self_name()} - {self.user.username}'
            else:
                return f'{self.parent.get_self_name()} - {self.name}'
        except AttributeError:
            if self.node_type == self.NodeType.PEOPLE:
                return f'{self.user.username}'
            else:
                return f'{self.name}'

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
    def get_origins():
        return Node.objects.filter(parent=None)

from itertools import chain

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class OrganisationalUnitModel(models.Model):
    name = models.CharField(max_length=150)


class Node(models.Model):
    """
        Implementation of adjacent list model
    """
    class NodeType(models.TextChoices):
        PEOPLE = 'PL', _('People')
        ORGANISATION = 'ORG', _('Organisational unit')

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE
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
    org_unit = models.ForeignKey(
        OrganisationalUnitModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

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

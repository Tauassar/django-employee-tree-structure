from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class OrganisationalUnitModel(models.Model):
    name = models.CharField(max_length=150)


class Node(models.Model):
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

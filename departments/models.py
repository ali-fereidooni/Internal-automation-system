from django.db import models
from accounts.models import User


class Department(models.Model):
    DEPARTMENTS_CHOICES = [
        ('manager', 'Manager'),
        ('develope', 'Develope'),
        ('sell', 'Sell'),
        ('marketing', 'Marketing'),
    ]

    name = models.CharField(
        max_length=10, choices=DEPARTMENTS_CHOICES, default=None, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    pass

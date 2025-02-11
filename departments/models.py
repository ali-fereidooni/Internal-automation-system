from django.db import models


class Department(models.Model):
    DEPARTMENTS_CHOICES = [
        ('manager', 'Manager'),
        ('develope', 'Develope'),
        ('sell', 'Sell'),
        ('marketing', 'Marketing'),
    ]

    department = models.CharField(
        max_length=10, choices=DEPARTMENTS_CHOICES, default='develope')


class Position(models.Model):
    pass

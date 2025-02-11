from django.db import models


class Department(models.Model):
    DEPARTMENTS_CHOICES = [
        ('manager', 'Manager'),
        ('develope', 'Develope'),
        ('sell', 'Sell'),
        ('marketing', 'Marketing'),
    ]

    departments = models.CharField(
        max_length=10, choices=DEPARTMENTS_CHOICES, default='manager')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.departments


class Position(models.Model):
    pass

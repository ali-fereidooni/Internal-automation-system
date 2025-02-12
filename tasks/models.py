from django.db import models
from accounts.models import User
from departments.models import Department
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Task(models.Model):
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    department = models.OneToOneField(
        Department, on_delete=models.CASCADE, related_name="tasks", to_field='name')
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usertasks")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pending')
    compeleted = models.BooleanField(default=False)
    due_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} "

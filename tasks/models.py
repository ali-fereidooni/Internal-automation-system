from django.db import models
from accounts.models import User


class Task(models.Model):
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    DEPARTMENTS_CHOICES = [
        ('manager', 'Manager'),
        ('develope', 'Develope'),
        ('sell', 'Sell'),
        ('marketing', 'Marketing'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    department = models.CharField(choices=DEPARTMENTS_CHOICES, max_length=20)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", default=None)
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

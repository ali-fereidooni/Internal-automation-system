from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"

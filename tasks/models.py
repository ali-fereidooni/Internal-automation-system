from django.db import models
from accounts.models import User
from departments.models import Projects


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
    project = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", default=None)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='pending')
    completed = models.BooleanField(default=False)
    due_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} "

    def save(self, *args, **kwargs):
        if self.completed:
            self.status = 'completed'
        super(Task, self).save(*args, **kwargs)

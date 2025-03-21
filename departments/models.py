from django.db import models
from accounts.models import User


class Departments(models.Model):
    NAME_CHOICES = [
        ('manager', 'Manager'),
        ('develope', 'Develope'),
        ('sell', 'Sell'),
        ('marketing', 'Marketing'),
    ]

    name = models.CharField(max_length=100, choices=NAME_CHOICES)
    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='department_manager')
    members = models.ManyToManyField(User, related_name='department_members')

    def __str__(self):
        return self.name


class Projects(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(
        Departments, on_delete=models.CASCADE, related_name='department_projects')
    members = models.ManyToManyField(
        User, related_name='project_members')

    def __str__(self):
        return self.name

    def progress_percentage(self):
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(status='completed').count()
        if total_tasks > 0:
            # درصد با دو رقم اعشار
            return round((completed_tasks / total_tasks) * 100, 2)
        return 0

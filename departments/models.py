from django.db import models


class Departments(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        'accounts.Employee', on_delete=models.CASCADE, related_name='department_manager')
    members = models.ManyToManyField(
        'accounts.Employee', related_name='department_members')

    def __str__(self):
        return self.name


class Projects(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Departments, on_delete=models.CASCADE, related_name='department_projects')
    members = models.ManyToManyField(
        'accounts.Employee', related_name='project_members')

    def __str__(self):
        return self.name

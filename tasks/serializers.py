from .models import Task, Department
from rest_framework import serializers
from .models import Task
from departments.models import Department
from django.shortcuts import get_object_or_404
from departments.serializers import DepartmentSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField()  # نمایش نام کارمند به جای ID
    # نمایش نام وضعیت به جای کد وضعیت
    status = serializers.CharField(source='get_status_display')
    # نمایش نام اولویت به جای کد اولویت
    priority = serializers.CharField(source='get_priority_display')
    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(),
        slug_field='departments'  # مقدار `str` به جای `id` برای دپارتمان
    )

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'assigned_to', 'department', 'priority',
                  'status', 'created_at', 'updated')
        read_only_fields = ['created_at', 'updated']

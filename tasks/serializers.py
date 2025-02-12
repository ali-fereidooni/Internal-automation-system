from .models import Task, Department
from rest_framework import serializers
from .models import Task
from departments.models import Department
from departments.serializers import DepartmentSerializer


class TaskSerializer(serializers.ModelSerializer):
    # assigned_to = serializers.StringRelatedField()  # نمایش نام کارمند به جای ID
    # department = serializers.StringRelatedField()  # نمایش نام دپارتمان به جای ID

    class Meta:
        model = Task
        fields = ('id', 'title', 'description',
                  'assigned_to', 'department', 'priority', 'status')
        read_only_fields = ['created_at', 'updated']

    '''def create(self, validated_data):
        # مقدار دسته‌بندی (رشته) را دریافت کن
        department_name = validated_data.pop('name')
        category, created = Department.objects.get_or_create(
            name=department_name)  # جستجو یا ایجاد دسته‌بندی
        validated_data['name'] = category  # مقدار را به ID تبدیل کن
        return Task.objects.create(**validated_data)  # تسک را ایجاد کن'''

    '''def get_name(self, obj):
        result = obj.get('name')
        return TaskSerializer(instance=result, many=True).data'''

from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField()  # نمایش نام کارمند به جای ID

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

from rest_framework import serializers
from .models import Task
from accounts.models import User
from departments.models import Projects


# نمایش نام کارمند به جای ID


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'role')


class ProjectSerializers(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('name', 'department', 'members')


class TaskCreateSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    project = ProjectSerializers()

    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'priority', 'user',
                  'status', 'created_at', 'updated')
        read_only_fields = ['created_at', 'updated']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())
    project = serializers.SlugRelatedField(
        slug_field='name', queryset=Projects.objects.all())

    class Meta:
        model = Task
        fields = ('title', 'description', 'project', 'priority', 'user',
                  'status', 'created_at', 'updated')
        read_only_fields = ['created_at', 'updated']

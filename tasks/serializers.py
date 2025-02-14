from rest_framework import serializers
from .models import Task
from accounts.models import User


# نمایش نام کارمند به جای ID


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'role')


class TaskCreateSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Task
        fields = ('title', 'description', 'department', 'priority', 'user',
                  'status', 'created_at', 'updated')
        read_only_fields = ['created_at', 'updated']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ('title', 'description', 'department', 'priority', 'user',
                  'status', 'created_at', 'updated')
        read_only_fields = ['created_at', 'updated']

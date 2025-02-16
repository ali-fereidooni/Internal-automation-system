from rest_framework import serializers
from .models import Projects, Departments
from accounts.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class ProjectCreateSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        slug_field='name', queryset=Departments.objects.all())
    members = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(), many=True)

    class Meta:
        model = Projects
        fields = '__all__'

from .models import Department
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('departments',)

    def create(self, validated_data):
        return Department.objects.create(**validated_data)

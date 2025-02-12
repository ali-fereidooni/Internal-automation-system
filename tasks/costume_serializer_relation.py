from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return f'{value.name}'

    def to_internal_value(self, data):
        return {'departments': data}

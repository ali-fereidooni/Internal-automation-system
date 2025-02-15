from rest_framework import serializers
from .models import LeaveRequest
from accounts.models import User


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ('status', 'employee')

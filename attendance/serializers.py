from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username instead of ID
    # Format work duration as HH:MM:SS
    work_duration = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'date', 'check_in',
                  'check_out', 'status', 'work_duration']
        # Prevent updating work_duration manually
        read_only_fields = ['work_duration']

    def get_work_duration(self, obj):
        """Format work_duration as HH:MM:SS"""
        if obj.work_duration:
            total_seconds = int(obj.work_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return "00:00:00"

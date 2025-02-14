from django.db import models

from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, time

User = get_user_model()


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('leave', 'On Leave'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(auto_now_add=True)  # تاریخ ورود (به‌صورت خودکار)
    check_in = models.TimeField(null=True, blank=True)  # ساعت ورود
    check_out = models.TimeField(null=True, blank=True)  # ساعت خروج
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='present')
    work_duration = models.DurationField(null=True, blank=True)  # مدت زمان کار

    def calculate_work_duration(self):
        """محاسبه مدت زمان کار براساس ساعت ورود و خروج"""
        if self.check_in and self.check_out:
            check_in_dt = datetime.combine(self.date, self.check_in)
            check_out_dt = datetime.combine(self.date, self.check_out)
            return check_out_dt - check_in_dt
        return None

    def save(self, *args, **kwargs):
        self.work_duration = self.calculate_work_duration()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"

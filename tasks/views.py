from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework import generics
from accounts.permissions import IsEmployee, IsManager


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # مدیران همه تسک‌ها را می‌بینند
            return Task.objects.all()
        # کارمندان فقط تسک‌های خودشان را ببینند
        return Task.objects.filter(assigned_to=user)


class CreateTaskView(generics.CreateAPIView):
    """ایجاد تسک جدید (فقط برای مدیران)"""
    serializer_class = TaskSerializer
    permission_classes = [IsManager]


class TaskListView(generics.ListAPIView):
    """مشاهده لیست تسک‌ها (همه کاربران)"""
    serializer_class = TaskSerializer
    permission_classes = [IsEmployee | IsManager]

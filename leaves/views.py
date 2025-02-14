from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework import generics
from accounts.permissions import IsEmployee, IsManager


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        # تنظیم کاربر فعلی به عنوان درخواست‌دهنده
        serializer.save(employee=self.request.user)


class RequestLeaveView(generics.CreateAPIView):
    """درخواست مرخصی (فقط برای کارمندان)"""
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsEmployee]


class ApproveLeaveView(generics.UpdateAPIView):
    """تأیید یا رد مرخصی (فقط برای مدیران)"""
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsManager]

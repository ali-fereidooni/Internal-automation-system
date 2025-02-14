from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework import generics, status
from accounts.permissions import IsEmployee, IsManager
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import DatabaseError


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]
    queryset = LeaveRequest.objects.all()

    def list(self, request, *args, **kwargs):
        requests = self.serializer_class(self.queryset, many=True).data
        try:
            return Response(requests)
        except LeaveRequest.DoesNotExist:
            return Response({'message': 'No leave request found'}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError:
            return Response({"error": "database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)


class RequestLeaveView(generics.CreateAPIView):
    """درخواست مرخصی (فقط برای کارمندان)"""
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsEmployee]


class CreateLeaveRequest(generics.CreateAPIView):
    """درخواست مرخصی (فقط برای کارمندان)"""
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)


class ApproveLeaveView(generics.UpdateAPIView):
    """تأیید یا رد مرخصی (فقط برای مدیران)"""
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsManager]

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

    def get(self, request, *args, **kwargs):
        list = LeaveRequest.objects.filter(employee=request.user)
        serializer = LeaveRequestSerializer(list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # داده‌های ورودی را دریافت می‌کنیم
        data = request.data

        # بررسی پر بودن فیلدها
        required_fields = ['leave_type', 'start_date', 'end_date', 'reason']
        missing_fields = [
            field for field in required_fields if field not in data or not data[field]]

        if missing_fields:
            return Response({"error": f"این فیلدها اجباری هستند: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.is_anonymous:  # بررسی مجدد برای جلوگیری از AnonymousUser
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        has_pending_request = LeaveRequest.objects.filter(
            employee=request.user, status="pending"
        ).exists()
        if has_pending_request:
            return Response({"error": "شما یک درخواست مرخصی در حال بررسی دارید"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            task = LeaveRequest.objects.create(
                employee=request.user,
                leave_type=data['leave_type'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                reason=data['reason'],
            )

        # سریالایزر برای بازگشت داده‌های تسک ایجاد شده
        serializer = LeaveRequestSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApproveLeaveView(generics.UpdateAPIView):
    """تأیید یا رد مرخصی (فقط برای مدیران)"""
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsManager]

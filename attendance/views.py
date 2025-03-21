from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from .models import Attendance
from .serializers import AttendanceSerializer
from accounts.permissions import IsAdmin, IsManager, IsHR


class CheckInView(APIView):
    """Allows users to check in (start work)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        today = now().date()

        # Check if the user has already checked in today
        attendance, created = Attendance.objects.get_or_create(
            user=user, date=today)

        if attendance.check_in:
            return Response({"message": "You have already checked in today!"}, status=400)

        # Set check-in time
        attendance.check_in = now().time()
        attendance.save()
        return Response({"message": "Check-in successful!", "data": AttendanceSerializer(attendance).data}, status=200)


class CheckOutView(APIView):
    """Allows users to check out (end work)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        today = now().date()

        try:
            attendance = Attendance.objects.get(user=user, date=today)
        except Attendance.DoesNotExist:
            return Response({"message": "You haven't checked in yet!"}, status=400)

        if attendance.check_out:
            return Response({"message": "You have already checked out today!"}, status=400)

        # Set check-out time
        attendance.check_out = now().time()
        attendance.save()
        return Response({"message": "Check-out successful!", "data": AttendanceSerializer(attendance).data}, status=200)


class WorkReportsViewsest(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdmin | IsManager | IsHR]

    def list(self, request):
        """
        گزارش کاری کاربر را بر اساس تاریخ برمی‌گرداند.
        """
        user_reports = Attendance.objects.filter(user=request.user)

        # سریالایز کردن داده‌ها
        response_data = {
            "reports": AttendanceSerializer(user_reports, many=True).data,
        }

        return Response(response_data)

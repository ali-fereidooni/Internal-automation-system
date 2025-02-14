from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from .models import Attendance
from .serializers import AttendanceSerializer


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

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework import generics, status
from accounts.permissions import IsEmployee, IsManager, IsHR, IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsManager | IsHR | IsAdmin]
    authentication_classes = [JWTAuthentication]
    queryset = LeaveRequest.objects.all()

    def list(self, request):
        """
        درخواست‌های کاربر را بر اساس وضعیت دسته‌بندی کرده و برمی‌گرداند.
        """
        user_requests = LeaveRequest.objects.all()

        # دسته‌بندی درخواست‌ها
        pending_requests = user_requests.filter(status="pending")
        approved_requests = user_requests.filter(status="approved")
        rejected_requests = user_requests.filter(status="rejected")

        # سریالایز کردن داده‌ها
        response_data = {
            "pending": LeaveRequestSerializer(pending_requests, many=True).data,
            "approved": LeaveRequestSerializer(approved_requests, many=True).data,
            "rejected": LeaveRequestSerializer(rejected_requests, many=True).data,
        }

        return Response(response_data)

    def post(self, request, *args, **kwargs):
        request_id = request.data.get("id")
        new_status = request.data.get("status")

        if new_status not in ["approved", "rejected"]:
            return Response({"error": "وضعیت نامعتبر است. فقط 'approved' یا 'rejected' مجاز است."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            leave_request = LeaveRequest.objects.get(id=request_id)
            leave_request.status = new_status
            leave_request.save()
            return Response({"message": f"درخواست با موفقیت {new_status} شد."}, status=status.HTTP_200_OK)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "درخواست موردنظر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)


class CreateLeaveRequest(generics.CreateAPIView):
    """درخواست مرخصی (فقط برای کارمندان)"""
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        user_requests = LeaveRequest.objects.filter(employee=request.user)

        # دسته‌بندی درخواست‌ها
        pending_requests = user_requests.filter(status="pending")
        approved_requests = user_requests.filter(status="approved")
        rejected_requests = user_requests.filter(status="rejected")

        # سریالایز کردن داده‌ها
        response_data = {
            "pending": LeaveRequestSerializer(pending_requests, many=True).data,
            "approved": LeaveRequestSerializer(approved_requests, many=True).data,
            "rejected": LeaveRequestSerializer(rejected_requests, many=True).data,
        }

        return Response(response_data)

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

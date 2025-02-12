from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
# ایجاد فایل permissions.py در users
from accounts.permissions import IsAdmin, IsManager
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from departments.models import Department


# 🔹 1️⃣ ایجاد تسک (فقط توسط مدیران)


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager | IsAdmin]

    def list(self, request):
        srz_data = TaskSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(Task, assigned_to=kwargs['assigned_to'])
        srz_data = TaskSerializer(instance=user)
        return Response(data=srz_data.data)

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=kwargs['pk'])
        srz_data = TaskSerializer(
            instance=user, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.is_active = False
        user.save()
        return Response({'message': 'task deleted'}, status=status.HTTP_200_OK)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdmin | IsManager]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        ser_data = TaskSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskStatusUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """کاربر فقط تسک‌های مربوط به خودش را تغییر دهد"""
        return Task.objects.filter(assigned_to=self.request.user)

    def update(self, request, *args, **kwargs):
        """اجازه تغییر فقط به فیلد status را بدهد"""
        task = self.get_object()
        if 'status' not in request.data:
            return Response({'error': 'فقط وضعیت تسک قابل تغییر است.'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = request.data['status']
        task.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

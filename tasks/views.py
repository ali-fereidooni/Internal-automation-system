from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
# ایجاد فایل permissions.py در users
from accounts.permissions import IsAdmin, IsManager

# 🔹 1️⃣ ایجاد تسک (فقط توسط مدیران)


class TaskViewset(viewsets.ModelViewSet):
    pass


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdmin | IsManager]

# 🔹 2️⃣ مشاهده لیست تسک‌های اختصاص داده شده به کاربر لاگین شده


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """فقط تسک‌های مربوط به کاربر لاگین شده را نمایش دهد"""
        return Task.objects.filter(assigned_to=self.request.user)

# 🔹 3️⃣ ویرایش و حذف تسک (فقط توسط مدیران)


class TaskUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdmin | IsManager]

# 🔹 4️⃣ تغییر وضعیت تسک توسط کارمندان


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

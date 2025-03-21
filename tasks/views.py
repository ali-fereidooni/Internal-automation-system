from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskCreateSerializer, TaskSerializer
# ایجاد فایل permissions.py در users
from accounts.permissions import IsAdmin, IsManager
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_list_or_404
from accounts.models import User
from departments.models import Projects


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
        user = get_object_or_404(Task, user=kwargs['user'])
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
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAdmin | IsManager]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        # ایجاد نمونه خالی از سریالایزر
        serializer = TaskCreateSerializer()

        # برگرداندن فیلدهای خالی
        empty_fields = {
            field_name: "This field is required !" for field_name in serializer.fields.keys()}

        # افزودن گزینه‌های کلید خارجی (لیست کاربران موجود)
        empty_fields["user_choices"] = [
            {"id": user.id, "username": user.username} for user in User.objects.all()
        ]

        return Response(empty_fields)

    def post(self, request, *args, **kwargs):
        # داده‌های ورودی را دریافت می‌کنیم
        data = request.data

        # بررسی پر بودن فیلدها
        required_fields = ['title', 'description', 'project', 'priority', 'user',
                           'status',]
        missing_fields = [
            field for field in required_fields if field not in data or not data[field]]

        if missing_fields:
            return Response({"error": f"این فیلدها اجباری هستند: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی اینکه آیا یوزر با ID داده شده وجود دارد
        try:
            user = User.objects.get(username=data['user'])
        except User.DoesNotExist:
            return Response({"error": "کاربر انتخاب شده وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)

        try:
            project = Projects.objects.get(name=data['project'])
        except Projects.DoesNotExist:
            return Response({"error": "این پروژه انتخاب شده وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)
    # ایجاد و ذخیره تسک در دیتابیس
        task = Task.objects.create(
            title=data['title'],
            description=data['description'],
            project=project,
            priority=data['priority'],
            user=user,
            status=data['status'],
        )

        # سریالایزر برای بازگشت داده‌های تسک ایجاد شده
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskListView(generics.ListAPIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


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
# Add finished projects and tasks

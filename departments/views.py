from rest_framework import viewsets, status
from accounts.permissions import IsAdmin, IsManager, IsHR
from .models import Projects, Departments
from .serializers import ProjectSerializer, ProjectCreateSerializer
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdmin | IsManager | IsHR]

    def list(self, request):
        """
        لیست تمام پروژه‌ها را برمی‌گرداند.
        """
        projects = Projects.objects.all()

        return Response(ProjectSerializer(projects, many=True).data)

    def create(self, request):
        """
        یک پروژه جدید ایجاد می‌کند.
        """
        data = request.data
        try:
            department = Departments.objects.get(name=data['department'])
        except Departments.DoesNotExist:
            return Response({"error": "این دپارتمان انتخاب شده وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

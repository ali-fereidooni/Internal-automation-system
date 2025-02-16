from rest_framework import viewsets, status
from accounts.permissions import IsAdmin, IsManager, IsHR
from .models import Projects, Departments
from .serializers import ProjectSerializer, ProjectCreateSerializer
from rest_framework.response import Response
from accounts.models import User


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
        open_project = Projects.objects.filter(
            name=data['name']
        ).exists()
        if open_project:
            return Response({"error": "درحال حاضر یک پروژه باز با این نام وجود دارد"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """
        اطلاعات یک پروژه را به‌روز می‌کند.
        """
        project = Projects.objects.get(id=pk)
        data = request.data
        try:
            department = Departments.objects.get(name=data['department'])
        except Departments.DoesNotExist:
            return Response({"error": "این دپارتمان انتخاب شده وجود ندارد."}, status=status.HTTP_404_NOT_FOUND)
        project.name = data['name']
        project.department = department
        project.members = data['members']
        project.save()
        serializer = ProjectCreateSerializer(project)
        return Response(serializer.data)

    def destroy(self, request, name):
        """
        یک پروژه را حذف می‌کند.
        """
        project = Projects.objects.get(name=name)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

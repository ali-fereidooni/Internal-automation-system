from rest_framework import viewsets
from accounts.permissions import IsAdmin, IsManager, IsHR
from .models import Projects
from .serializers import ProjectSerializer
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
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

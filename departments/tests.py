from django.urls import path, include
from django.test import TestCase
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='admins')

app_name = 'departments'
url_patterns = [
    path('projects/', include(router.urls)),
]

from django.urls import path, include
from .views import ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='admins')

app_name = 'departments'
url_patterns = [
    path('projects/', include(router.urls)),
]

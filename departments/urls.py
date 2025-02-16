from django.urls import path, include
from .views import ProjectViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'project', ProjectViewSet, basename='project')

app_name = 'departments'
urlpatterns = [
    path('', include(router.urls)),
]

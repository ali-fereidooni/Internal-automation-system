from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewset, TaskCreateView

router = DefaultRouter()
router.register(r'tasks', TaskViewset, basename='tasks')
app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls)),
    path('create/', TaskCreateView.as_view(), name='create_task'),
]

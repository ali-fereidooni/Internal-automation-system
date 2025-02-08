from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CreateTaskView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

'''app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreateTaskView.as_view(), name="create-task"),
]'''

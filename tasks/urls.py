from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewset

router = DefaultRouter()
router.register(r'tasks', TaskViewset, basename='tasks')
app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls))
]

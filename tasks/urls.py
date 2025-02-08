from django.urls import path
from .views import TaskCreateView, TaskListView, TaskUpdateDeleteView, TaskStatusUpdateView

app_name = 'tasks'
urlpatterns = [
    path('create/', TaskCreateView.as_view(), name="task-create"),
    path('my-tasks/', TaskListView.as_view(), name="task-list"),
    path('<int:pk>/', TaskUpdateDeleteView.as_view(), name="task-update-delete"),
    path('<int:pk>/update-status/', TaskStatusUpdateView.as_view(),
         name="task-status-update"),
]

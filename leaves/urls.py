from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveRequestViewSet, CreateLeaveRequest

router = DefaultRouter()
router.register(r'admins', LeaveRequestViewSet, basename='admins')

app_name = 'leaves'
urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreateLeaveRequest.as_view(), name='create'),

]

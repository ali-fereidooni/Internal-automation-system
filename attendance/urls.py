from django.urls import path, include
from .views import CheckInView, CheckOutView, WorkReportsViewsest
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admins', WorkReportsViewsest, basename='admins')


app_name = 'attendance'
urlpatterns = [
    path('', include(router.urls)),
    path('check-in/', CheckInView.as_view(), name='check-in'),
    path('check-out/', CheckOutView.as_view(), name='check-out'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, RegisterView, UserListView, UserProfileView, LoginView

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='accounts')

app_name = 'accounts'
urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('users/', UserListView.as_view(), name="user-list"),
    path('profile/', UserProfileView.as_view(), name="profile"),
]

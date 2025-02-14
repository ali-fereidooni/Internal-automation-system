from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import AdminUserViewSet, UserRegister, UserProfileView, LoginView

router = SimpleRouter()
router.register(r'adminuser', AdminUserViewSet, basename='adminuser')

app_name = 'accounts'
urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegister.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # ورود و دریافت توکن
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),  # دریافت توکن جدید
    path('token/verify/', TokenVerifyView.as_view(),
         name='token_verify'),  # بررسی اعتبار توکن
]

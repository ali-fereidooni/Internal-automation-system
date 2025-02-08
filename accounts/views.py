from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserRegisterSerializer, UserProfileSerializer, LoginSerializer
from .models import User
from .permissions import IsAdmin, IsManager, IsHR
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import status


# ViewSet برای مشاهده و مدیریت کاربران


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # فقط ادمین می‌تواند کاربران را مدیریت کند
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager | IsAdmin | IsHR]


# API برای ثبت‌نام کاربر


class UserListView(generics.ListAPIView):
    """مشاهده لیست کاربران (فقط برای ادمین‌ها)"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsManager | IsAdmin | IsHR]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        srz_data = UserRegisterSerializer(data=request.POST)
        if srz_data.is_valid():
            srz_data.create(srz_data.validated_data)

            return Response(data=srz_data.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """نمایش و ویرایش پروفایل کاربر"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """برگرداندن پروفایل مربوط به کاربر لاگین شده"""
        return self.request.user


class LoginView(generics.GenericAPIView):
    """ویو برای ورود کاربران و دریافت توکن JWT"""
    serializer_class = LoginSerializer
    # همه کاربران می‌توانند وارد شوند
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

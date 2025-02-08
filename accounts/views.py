from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer
from .models import User
from .permissions import IsAdmin, IsManager, IsHR
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        response.data['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return response


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

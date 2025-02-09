from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserRegisterSerializer, UserSerializer, LoginSerializer, UserProfileSerializer
from .models import User
from .permissions import IsAdmin, IsManager, IsHR
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


from rest_framework import status


# ViewSet برای مشاهده و مدیریت کاربران


class UserRegister(APIView):
    permission_classes = [IsHR]

    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """ویو برای ورود کاربران و دریافت توکن JWT"""
    serializer_class = LoginSerializer
    # همه کاربران می‌توانند وارد شوند
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager | IsAdmin | IsHR]

    def list(self, request):
        srz_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        srz_data = UserSerializer(instance=user)
        return Response(data=srz_data.data)

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(self.queryset, pk=kwargs['pk'])
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'}, status=status.HTTP_403_FORBIDDEN)
        srz_data = UserSerializer(
            instance=user, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.is_active = False
        user.save()
        return Response({'message': 'user deactivated'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    # فقط کاربران احراز هویت شده دسترسی دارند
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        if request.user.is_anonymous:  # بررسی مجدد برای جلوگیری از AnonymousUser
            return Response({"error": "User not authenticated"}, status=401)

        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

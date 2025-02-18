from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserRegisterSerializer, UserSerializer, LoginSerializer, ProfileSerializer
from .models import User, Profile
from .permissions import IsAdmin, IsManager, IsHR
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


# ViewSet برای مشاهده و مدیریت کاربران


class UserRegister(APIView):
    permission_classes = [IsHR | IsAdmin]

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
        user = get_object_or_404(User, username=kwargs['username'])
        srz_data = UserSerializer(instance=user)
        return Response(data=srz_data.data)

    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(self.queryset, username=kwargs['username'])
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


class ProfileView(APIView):
    permission_classes = [IsAdmin | IsManager | IsHR]
    queryset = Profile.objects.all()

    def get(self, request):
        srz_data = ProfileSerializer(instance=self.queryset.all(), many=True)
        return Response(data=srz_data.data)


class ProfilePictureUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.profile_picture = request.data.get('profile_picture')
        user.save()
        return Response({"message": "Profile picture updated successfully"}, status=status.HTTP_200_OK)

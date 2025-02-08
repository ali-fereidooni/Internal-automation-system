from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',  'first_name',
                  'last_name', 'phone_number', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'phone_number',
                  'email', 'password', 'confirm_password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def clean_password2(self):
        cd = self.validated_data
        if cd['password'] and cd['confirm_password'] and cd['password'] != cd['confirm_password']:
            raise ValidationError('passwords didnt match')
        return cd['confirm_password']

    def save(self):
        user = super().save()
        user.set_password(self.validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # بررسی نام کاربری و رمز عبور
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                "نام کاربری یا رمز عبور نادرست است.")

        # ایجاد توکن‌های JWT
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            }
        }

from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError


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

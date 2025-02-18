from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


import os
from django.utils.timezone import now


class User(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('hr', 'HR'),
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number',]

    def __str__(self):
        return f"{self.username}- {self.role}"

    @property
    def is_staff(self):
        return self.is_admin

    def is_admin(self):
        return self.role == 'admin'

    def is_manager(self):
        return self.role == 'manager'

    def is_hr(self):
        return self.role == 'hr'

    def is_employee(self):
        return self.role == 'employee'


def user_directory_path(instance, filename):
    # نام فایل را تغییر می‌دهیم تا از تکرار جلوگیری شود
    ext = filename.split('.')[-1]
    filename = f"profile_{now().strftime('%Y%m%d%H%M%S')}.{ext}"

    # مسیر ذخیره‌سازی: media/profile_pictures/user_<id>/profile_xxx.jpg
    return os.path.join('profile_pictures', f'user_{instance.id}', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

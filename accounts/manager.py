from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, email, password, **extra_fields):
        if not username:
            raise ValueError('you must have fullname')
        if not email:
            raise ValueError('you must have email')
        if not phone_number:
            raise ValueError('you must have phone number')

        user = self.model(username=username, phone_number=phone_number, email=self.normalize_email(email), **extra_fields
                          )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, phone_number, email, password):
        user = self.create_user(username, phone_number,
                                email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user

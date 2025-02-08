from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('role',)
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Main', {'fields': ('username', 'email',
         'phone_number', 'role', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',
         'last_login', 'groups', 'user_permissions')}),

    )

    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number',
         'role', 'password1', 'password2')}),
    )

    search_fields = ('email', 'username', 'phone_number', 'role')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.register(User, UserAdmin)

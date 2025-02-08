from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """دسترسی فقط برای ادمین‌ها"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsManager(BasePermission):
    """دسترسی فقط برای مدیران"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager()


class IsHR(BasePermission):
    """دسترسی فقط برای کارمندان امور اداری"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_hr()


class IsEmployee(BasePermission):
    """دسترسی فقط برای کارمندان"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_employee()

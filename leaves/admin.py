from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'status')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__username', 'leave_type', 'status')
    readonly_fields = ('status', 'employee')

from django.contrib import admin
from .models import Task

# Register your models here.


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ('title', 'priority', 'assigned_to')
    search_fields = ('assigned_to',)
    list_filter = ('updated', 'priority')

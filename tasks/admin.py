from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'due_date', 'is_completed', 'priority', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username')
    list_filter = ('is_completed', 'priority', 'due_date', 'created_at')
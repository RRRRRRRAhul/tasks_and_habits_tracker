from django.contrib import admin
from .models import Habit, HabitLog

# Register your models here.
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'frequency', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username')
    list_filter = ('frequency', 'is_active', 'created_at')

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit', 'date', 'count', 'created_at')
    search_fields = ('habit__name',)
    list_filter = ('date', 'created_at')
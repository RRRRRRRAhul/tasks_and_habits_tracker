from rest_framework import serializers

class TaskAnalyticsSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    completion_percentage = serializers.FloatField()

class TodayHabitAnalyticsSerializer(serializers.Serializer):
    total_active_habits = serializers.IntegerField()
    completed_today = serializers.IntegerField()
    missed_today = serializers.IntegerField()

class HabitStreakAnalyticsSerializer(serializers.Serializer):
    habit_id = serializers.IntegerField()
    habit_name = serializers.CharField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()

class WeeklyHabitAnalyticsSerializer(serializers.Serializer):
    habit_id = serializers.IntegerField()
    habit_name = serializers.CharField()
    completed_days = serializers.IntegerField()
    total_days = serializers.IntegerField()
    success_rate = serializers.FloatField()

class HabitIntensityAnalyticsSerializer(serializers.Serializer):
    habit_id = serializers.IntegerField()
    habit_name = serializers.CharField()
    total_count = serializers.IntegerField()
    average_count_per_day = serializers.FloatField()

from rest_framework import serializers
from .models import Habit, HabitLog


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ["id", "name", "frequency", "is_active", "created_at", "updated_at"]

    def validate_frequency(self, value):
        if value not in ["daily", "weekly"]:
            raise serializers.ValidationError(
                "Frequency must be either 'daily' or 'weekly'."
            )
        return value


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ["id", "date", "count", "created_at"]

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError("Count must be at least 1.")
        return value

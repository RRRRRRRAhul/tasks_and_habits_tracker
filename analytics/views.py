from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from tasks.models import Task
from habits.models import Habit, HabitLog
from .serializers import (
    TaskAnalyticsSerializer,
    TodayHabitAnalyticsSerializer,
    HabitStreakAnalyticsSerializer,
    WeeklyHabitAnalyticsSerializer,
    HabitIntensityAnalyticsSerializer,
)
from datetime import date, timedelta
from django.utils.timezone import now
from collections import defaultdict


class TaskAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        task = Task.objects.filter(user=request.user)
        total_tasks = task.count()
        completed_tasks = task.filter(is_Completed=True).count()
        pending_tasks = total_tasks - completed_tasks
        completion_percentage = (
            (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        )

        data = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_percentage": completion_percentage,
        }

        serializer = TaskAnalyticsSerializer(data)
        return Response(serializer.data)

class TodayHabitAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today = date.today()

        active_habits = Habit.objects.filter(
            user=request.user,
            is_active=True
        )

        total_active_habits = active_habits.count()

        completed_today = HabitLog.objects.filter(
            habit__in=active_habits,
            date=today
        ).values("habit").distinct().count()

        missed_today = total_active_habits - completed_today

        data = {
            "total_active_habits": total_active_habits,
            "completed_today": completed_today,
            "missed_today": missed_today,
        }

        serializer = TodayHabitAnalyticsSerializer(data)
        return Response(serializer.data)
    
class HabitStreakAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        habits = Habit.objects.filter(user=request.user)
        response = []

        for habit in habits:
            logs = HabitLog.objects.filter(habit=habit).order_by('-date')
            streak = 0
            longest_streak = 0
            previous_date = None
            for log in logs:
                if previous_date is None or (previous_date - log.date).days == 1:
                    streak += 1
                else:
                    longest_streak = max(longest_streak, streak)
                    streak = 1
                previous_date = log.date
            
            longest_streak = max(longest_streak, streak)
            response.append({
                "habit_id": habit.id,
                "habit_name": habit.name,
                "current_streak": streak,
                "longest_streak": longest_streak,
            })
        serializer = HabitStreakAnalyticsSerializer(response, many=True)
        return Response(serializer.data)
    
class WeeklyHabitAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        end_date = date.today()
        start_date = end_date - timedelta(days=6)

        habits = Habit.objects.filter(user=request.user)
        response = []

        for habit in habits:
            logs = HabitLog.objects.filter(
                habit=habit,
                date__range=(start_date, end_date)
            ).values_list('date', flat=True)

            completed_days = len(set(logs))
            total_days = 7
            success_rate = (completed_days / total_days) * 100 if total_days > 0 else 0

            response.append({
                "habit_id": habit.id,
                "habit_name": habit.name,
                "completed_days": completed_days,
                "total_days": total_days,
                "success_rate": success_rate,
            })

        serializer = WeeklyHabitAnalyticsSerializer(response, many=True)
        return Response(serializer.data)
    
class HabitIntensityAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        habits = Habit.objects.filter(user=request.user)
        response = []

        for habit in habits:
            logs = HabitLog.objects.filter(habit=habit)
            total_count = logs.aggregate(total=Sum('count'))['total'] or 0
            days_logged = logs.values('date').distinct().count()
            average_count_per_day = (total_count / days_logged) if days_logged > 0 else 0

            response.append({
                "habit_id": habit.id,
                "habit_name": habit.name,
                "total_count": total_count,
                "average_count_per_day": average_count_per_day,
            })

        serializer = HabitIntensityAnalyticsSerializer(response, many=True)
        return Response(serializer.data)
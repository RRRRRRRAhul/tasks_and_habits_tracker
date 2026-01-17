from django.urls import path
from .views import (
    TaskAnalyticsView,
    TodayHabitAnalyticsView,
    HabitStreakAnalyticsView,
    WeeklyHabitAnalyticsView,
    HabitIntensityAnalyticsView,
)

urlpatterns = [
    path("tasks/", TaskAnalyticsView.as_view()),
    path("habits/today/", TodayHabitAnalyticsView.as_view()),
    path("habits/streaks/", HabitStreakAnalyticsView.as_view()),
    path("habits/weekly/", WeeklyHabitAnalyticsView.as_view()),
    path("habits/intensity/", HabitIntensityAnalyticsView.as_view()),
]

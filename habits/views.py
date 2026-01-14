from rest_framework import generics, permissions
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer
from .permissions import HabitOwnerPermission, HabitLogOwnerPermission

class HabitData(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class HabitDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, HabitOwnerPermission]
    serializer_class = HabitSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
    
class HabitLogData(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, HabitLogOwnerPermission]
    serializer_class = HabitLogSerializer

    def get_queryset(self):
        habit_id = self.kwargs.get('habit_id')
        return HabitLog.objects.filter(habit__id=habit_id, habit__user=self.request.user)
    
    def perform_create(self, serializer):
        habit_id = self.kwargs.get('habit_id')
        habit = generics.get_object_or_404(Habit, id=habit_id, user=self.request.user)
        serializer.save(habit=habit)
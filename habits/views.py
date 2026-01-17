from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer
from .permissions import HabitOwnerPermission, HabitLogOwnerPermission

class HabitData(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HabitSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_completed', 'priority', 'due_date']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']

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
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['notes']
    ordering_fields = ['created_at']

    def get_queryset(self):
        habit_id = self.kwargs.get('habit_id')
        return HabitLog.objects.filter(habit__id=habit_id, habit__user=self.request.user)
    
    def perform_create(self, serializer):
        habit_id = self.kwargs.get('habit_id')
        habit = generics.get_object_or_404(Habit, id=habit_id, user=self.request.user)
        serializer.save(habit=habit)
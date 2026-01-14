from rest_framework.permissions import BasePermission

class HabitOwnerPermission(BasePermission):
    """
    Custom permission to only allow owners of a habit to access or edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class HabitLogOwnerPermission(BasePermission):
    """
    Custom permission to only allow owners of a habit log to access or edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.habit.user == request.user
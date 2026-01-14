from rest_framework.permissions import BasePermission

class TaskOwnerPermission(BasePermission):
    """
    Custom permission to only allow owners of a task to access or edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
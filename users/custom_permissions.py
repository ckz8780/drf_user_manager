from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Returns true if the user is the owner of the object, or is an admin
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class IsNotSameUser(BasePermission):
    """
    Returns true if user is not the object subject.
    Verifies that users can't delete themselves.
    """
    def has_object_permission(self, request, view, obj):
        return request.user != obj
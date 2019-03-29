from rest_framework import permissions

class IsProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'DELETE']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user)
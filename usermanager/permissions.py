from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
        
    def has_object_permission(self, request, view, obj):
        return bool(obj.owner == request.user)
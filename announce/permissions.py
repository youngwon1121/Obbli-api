from rest_framework import permissions
from django.shortcuts import get_object_or_404
from usermanager.models import Profile

class ReadForAnyAndWriteForAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return True
        else :
            return False
    
    def has_object_permission(self, request, view, obj):
        return False

class IsProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        profile = get_object_or_404(Profile, pk=request.data.get('profile'))
        if profile.owner == request.user:
            return True
        return False
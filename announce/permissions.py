from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.http import HttpResponseServerError
from usermanager.models import Profile
from .models import Announce

class IsProfileOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        profile = get_object_or_404(Profile, pk=request.data.get('profile'))
        if profile.owner != request.user:
            self.message = 'The profile is not yours. Use your profile'
            return False
        return True

class HaveApplied(permissions.BasePermission):
    def has_permission(self, request, view):
        #applying_list = Applying.objects.filter(announce_id=view.kwargs.get('pk')).select_related()
        applying_list = get_object_or_404(Announce, pk=view.kwargs.get('pk')).applying.all().select_related()
        for applying in applying_list:
            if applying.applier == request.user:
                self.message = 'You\'ve already applied.'
                return False
        return True
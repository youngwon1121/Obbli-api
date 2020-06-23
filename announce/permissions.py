from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.http import HttpResponseServerError
from .models import Announce

class IsAnnounceOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.writer == request.user)

class IsCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.writer == request.user)

class HaveApplied(permissions.BasePermission):
    def has_permission(self, request, view):
        announce = Announce.objects.prefetch_related('applying', 'applying__applier').get(pk=view.kwargs.get('pk'))
        applying_list = announce.applying.all()
        for applying in applying_list:
            if applying.applier == request.user:
                self.message = 'You\'ve already applied.'
                return False
        return True
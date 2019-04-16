from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from usermanager.models import Profile
from .serializers import AnnounceSerializer, ApplyingSerializer, CommentSerializer
from .models import Announce, Applying, Comment
from .permissions import IsProfileOwner, HaveApplied

User = get_user_model()

class AnnounceList(generics.ListCreateAPIView):
    serializer_class = AnnounceSerializer
    queryset = Announce.objects.all()

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

class AnnounceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnounceSerializer
    queryset = Announce.objects.all()

class CommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        parent = None
        if self.request.data.get('parent') is not None:
            parent_id = self.request.data.get('parent')
            parent = Comment.objects.get(pk=parent_id)
        announce = Announce.objects.get(pk=self.request.parser_context.get('kwargs').get('pk'))
        serializer.save(
            announce = announce,
            writer = self.request.user,
            parent = parent
        )

class CommentDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
class ApplyingAnnounce(generics.CreateAPIView):
    serializer_class = ApplyingSerializer
    queryset = Applying.objects.all()
    permission_classes = (IsAuthenticated, IsProfileOwner, HaveApplied,)

    def perform_create(self, serializer):
        announce = get_object_or_404(Announce, pk=self.request.parser_context.get('kwargs').get('pk')) 
        serializer.save(announce=announce, applier=self.request.user)
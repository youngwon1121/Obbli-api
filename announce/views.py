from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.shortcuts import Http404
from rest_framework import generics, exceptions
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from usermanager.models import Profile
from .serializers import AnnounceSerializer, ApplyingSerializer, CommentSerializer, AnnounceSerializerForList
from .models import Announce, Applying, Comment
from .permissions import HaveApplied, IsAnnounceOwner, IsCommentOwner

User = get_user_model()

class AnnounceList(generics.ListCreateAPIView):
    serializer_class = AnnounceSerializerForList

    def get_queryset(self):
        if self.request.query_params.get('type') in dict(Announce.INSTRUMENTAL_TYPES):
            return Announce.objects.filter(instrumental_type=self.request.query_params['type'])\
                .select_related('writer').order_by('-created_at')
        return Announce.objects.select_related('writer').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

class AnnounceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnounceSerializer
    queryset = Announce.objects.all()
    permission_classes = (IsAnnounceOwner,)

    def get_object(self):
        try:
            obj = Announce.objects.select_related('writer')\
                .prefetch_related('comments__replies', 'comments__writer', 'comments__replies__writer')\
                .get(pk=self.kwargs['pk'])
            if self.request.method in ['PUT', 'DELETE']:
                self.check_object_permissions(self.request, obj) 
            return obj

        except Announce.DoesNotExist:
            raise Http404

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
    permission_classes = (IsCommentOwner,)
    
class ApplyingAnnounce(generics.CreateAPIView):
    serializer_class = ApplyingSerializer
    queryset = Applying.objects.all()
    permission_classes = (IsAuthenticated, HaveApplied,)

    def perform_create(self, serializer):
        #profile owner check
        profile = Profile.objects.select_related('owner').get(pk=self.request.data.get('profile'))
        if profile.owner != self.request.user:
            raise exceptions.ParseError()

        announce = get_object_or_404(Announce, pk=self.request.parser_context.get('kwargs').get('pk'))
        serializer.save(announce=announce, applier=self.request.user)
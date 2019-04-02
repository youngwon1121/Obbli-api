from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from usermanager.models import Profile
from .serializers import AnnounceSerializer, ApplyingSerializer
from .models import Announce, Applying
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
    
class ApplyingAnnounce(generics.CreateAPIView):
    serializer_class = ApplyingSerializer
    queryset = Applying.objects.all()
    permission_classes = (IsAuthenticated, IsProfileOwner, HaveApplied,)

    def perform_create(self, serializer):
        #print(self.request.__dict__)
        announce = get_object_or_404(Announce, pk=self.request.parser_context.get('kwargs').get('pk')) 
        serializer.save(announce=announce, applier=self.request.user)